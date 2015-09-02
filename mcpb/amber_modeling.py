"""
This module contains the function to model leap input files for use.
"""
from __future__ import absolute_import, print_function
from msmtmol.mol import get_reslist
from msmtmol.readpdb import get_atominfo_fpdb, writepdb
from msmtmol.readmol2 import get_atominfo
from msmtmol.getlist import get_mc_blist
from msmtmol.element import resnamel, IonHFEparal, IonCMparal, IonIODparal
from mcpb.rename_residues import rename_res, get_diS_bond
from pymsmtexp import *
import warnings
import os

##############################################################################
# Related functions
##############################################################################
def gene_ion_libfile(resname, atname, element, charge):

    atomtyp = element + str(charge) + '+'
    ionfname = '%s.cmd' %resname

    ionf = open(ionfname, 'w')
    print('i = createAtom   %s  %s  %s' %(atname, atomtyp, str(charge)), file=ionf)
    print('set i    element %s' %element, file=ionf)
    print('set i    position { 0 0 0 }', file=ionf)
    print('r = createResidue %s' %resname, file=ionf)
    print('add r i', file=ionf)
    print('%s = createUnit %s' %(resname, resname), file=ionf)
    print('add %s r' %resname, file=ionf)
    print('saveOff %s ./%s' %(resname, resname + '.lib'), file=ionf)
    print('quit', file=ionf)
    ionf.close()

    os.system('tleap -s -f %s.cmd > %s.log' %(resname, resname))

def get_frcmod_fname(element, charge, watermodel, paraset):
    ##Get the frcmod file which will be loaded
    #Check whether there is parameter for the ion

    atomtyp0 = element + str(charge)

    if paraset in ['iod', '12_6_4']:
        if atomtyp0 not in IonIODparal:
            raise pymsmtError('There is no %s parameter set for %s ion with '
                              '%+d charge for %s water model in the '
                              'database.' \
                              %(paraset.upper(), element, charge, watermodel))
    if paraset in ['hfe']:
        if atomtyp0 not in IonHFEparal:
            raise pymsmtError('There is no %s parameter set for %s ion with '
                              '%+d charge for %s water model in the '
                              'database.' \
                              %(paraset.upper(), element, charge, watermodel))
    if paraset in ['cm']:
        if charge in [1, -1]:
            warnings.warn('There is no CM parameter set for %+d ions. '
                          'Here use HFE parameter set instead, as '
                          'author suggested.' %charge, pymsmtWarning)
            paraset = 'hfe' #For +1 ion, hfe is the default
        elif charge in [3, 4]:
            warnings.warn('There is no CM parameter set for %+d ions. '
                          'Here use IOD parameter set instead, as author '
                          'suggested.' %charge, pymsmtWarning)
            paraset = 'iod' #For +1 ion, iod is the default
        elif charge == 2:
            if atomtyp0 not in IonCMparal:
                raise pymsmtError('There is no %s parameter set for %s ion with '
                                  '%+d charge for %s water model in the '
                                  'database.' \
                                  %(paraset, element, charge, watermodel))

    #For +1 metal ions
    if charge in [1, -1]:
        frcmodf = 'frcmod.ions1lsm_'
        if paraset == 'hfe':
            frcmodf = frcmodf + paraset + '_' + watermodel
        elif paraset == 'iod':
            frcmodf = frcmodf + paraset
        elif paraset == '12_6_4':
            frcmodf = frcmodf + '1264_' + watermodel
    #For +2 metal ions, cm is the default
    elif charge == 2:
        frcmodf = 'frcmod.ionslrcm_'
        if paraset in ['hfe', 'cm']:
            frcmodf = frcmodf + paraset + '_' + watermodel
        elif paraset == 'iod':
            frcmodf = frcmodf + paraset
        elif paraset == '12_6_4':
            frcmodf = 'frcmod.ionslm_'
            frcmodf = frcmodf + '1264_' + watermodel
    #For +3 and +4 metal ions
    elif charge in [3, 4]:
        frcmodf = 'frcmod.ions34lsm_'
        if paraset == 'hfe':
            frcmodf = frcmodf + paraset + '_' + watermodel
        elif paraset == 'iod':
            frcmodf = frcmodf + 'iod'
        elif paraset == '12_6_4':
            frcmodf = frcmodf + '1264_' + watermodel

    return frcmodf

##############################################################################
#The following function has ability to generate three different leaprc files
#with model variable to switch them:
#0) For the bonded model with refitting the charge
#1) For the normal nonbonded model with refitting the charge
#2) For the normal nonbonded model without refitting the charge
##############################################################################

def gene_leaprc(gname, orpdbf, fipdbf, stpdbf, stfpf, ionids,\
                ionmol2fs, ioninf, mcresname, naamol2fs, ff_choice, frcmodfs,
                finfcdf, ileapf, model, watermodel='tip3p', paraset='cm'):

    print("******************************************************************")
    print("*                                                                *")
    print("*=================Generating input file for leap=================*")
    print("*                                                                *")
    print("******************************************************************")

    #---------------------Generate the new pdb file--------------------------
    #mol0 is the old mol while mol is new mol file with new names

    mol0, atids0, resids0 = get_atominfo_fpdb(orpdbf)

    reslist0 = get_reslist(mol0, resids0)

    mol, atids, resids = get_atominfo_fpdb(orpdbf)

    #rename the residue names into AMBER style, e.g. HIS --> HID, HIP, HIE
    mol = rename_res(mol, atids)

    #get the disulfur bond information
    disul = get_diS_bond(mol, atids)

    #resname the old residue names to new ones if it is not metal ion
    if model in [1, 2]:
        metcenres1 = [] #Old residue ids
        fp = open(stfpf, 'r')
        for line in fp:
            if line[0:4] != "LINK":
                line = line.split('-')
                if int(line[0]) not in metcenres1:
                    metcenres1.append(int(line[0]))
        fp.close()
        metcenres2 = mcresname #New residue names
        resndict = {}
        resns = []
        for i in range(0, len(metcenres1)):
            resndict[metcenres1[i]] = metcenres2[i]
            resns.append(metcenres2[i])

        for i in resndict.keys():
            mol.residues[i].resname = resndict[i]

    writepdb(mol, atids, fipdbf)
    #----------------------------get the atom names which changed atom type
    if model in [1, 2]:
        atomdefs = {}
        fp0 = open(stfpf, 'r')
        for line in fp0:
            if line[0:4] != "LINK":
                line = line.strip('\n')
                line = line.split()
                if line[2] != line[4]:
                    atnewtype = line[4]
                    element = mol.atoms[int(line[1])].element
                    if atnewtype not in atomdefs.keys():
                        atomdefs[atnewtype] = element
                    else:
                        if element != atomdefs[atnewtype]:
                            raise pymsmtError('There are atoms in fingerprint file '
                                              'of standard model with same atom type '
                                              'but different element.')
        fp0.close()
    #---------------------Get the bond information, mol2 is the standard model

    if model == 1:
        mol2, atids2, resids2 = get_atominfo_fpdb(stpdbf)
        blist = get_mc_blist(mol2, atids2, ionids, stfpf)
        blist1 = [(i[0], i[1]) for i in blist]

    #----------------------Generate the lib file and get the frcmod file name
    if model == 2:
        frcmodfs = []
        for ionmol2f in ionmol2fs:
            ionmol, ionatids, ionresids = get_atominfo(ionmol2f)
            for i in ionatids:
                element = ionmol.atoms[i].element
                chg = int(ionmol.atoms[i].charge)
                frcmodf = get_frcmod_fname(element, chg, watermodel, paraset)
                if frcmodf not in frcmodfs:
                    frcmodfs.append(frcmodf)
    elif model == 3 and ioninf != []:
        #get the metal information
        metresns = ioninf[0::4]
        metatns = ioninf[1::4]
        metelmts = ioninf[2::4]
        metelmts = [i[0] + i[1:].lower() for i in metelmts]
        metchgs = ioninf[3::4]
        metchgs = [int(i) for i in metchgs]
        #check the charge of the metal ions
        for metchg in metchgs:
            if metchg < -1 or metchg > 4:
                raise pymsmtError('Could not deal with atomic ion which has charge '
                                  'less than -1 or bigger than +4.')
        frcmodfs = []
        for i in range(0, len(metresns)):
            if metchgs[i] > 1: #if it is -1 or +1 ions, no need to create the lib file
                gene_ion_libfile(metresns[i], metatns[i], metelmts[i], metchgs[i])
                frcmodf = get_frcmod_fname(metelmts[i], metchgs[i], watermodel, paraset)
                if frcmodf not in frcmodfs:
                    frcmodfs.append(frcmodf)

    #-----------------------Generate the leap input file-----------------------

    print('Generating the leap input file...')

    ##Generate the tleap.in file
    lp = open(ileapf, 'w')
    if ff_choice in ['ff94', 'ff99', 'ff99SB', 'ff03', 'ff10']:
        print('source oldff/leaprc.%s' %ff_choice, file=lp)
    elif ff_choice in ['ff03.r1', 'ff12SB', 'ff14SB']:
        print('source leaprc.%s' %ff_choice, file=lp)
    print('source leaprc.gaff', file=lp)
    #Add atom types, for bonded model
    if model in [1, 2]:
        if atomdefs.keys() != []:
            print('addAtomTypes {', file=lp)
            for i in sorted(list(atomdefs.keys())):
                print('        { "%s"  "%s" "sp3" }' %(i, atomdefs[i]), file=lp)
            print('}', file=lp)

    #load lib and frcmod files for monovalent ions (for salt)
    if ff_choice in ['ff94', 'ff99', 'ff99SB', 'ff03', 'ff03.r1']:
        print('loadoff atomic_ions.lib', file=lp)
    print('loadamberparams frcmod.ions1lsm_hfe_%s' %watermodel, file=lp)

    #Load mol2 file for the refitting charge residues
    if model in [1, 2]:
        for i in resns:
            print('%s = loadmol2 %s.mol2' %(i, i), file=lp)
    elif model == 3:
        for i in naamol2fs:
            print('%s = loadmol2 %s.mol2' %(i, i), file=lp)

    #Load frcmod files for non-standard residues and metal site
    for i in frcmodfs:
        print('loadamberparams %s' %i, file=lp)

    if model == 1:
        print('loadamberparams %s' %finfcdf, file=lp)
    elif model == 2:
        for frcmodf in frcmodfs:
            print('loadamberparams %s' %frcmodf, file=lp)
    elif model == 3:
        for metresn in metresns:
            print('loadoff %s.lib' %metresn, file=lp)
        for frcmodf in frcmodfs:
            print('loadamberparams %s' %frcmodf, file=lp)

    #load pdb file
    print('mol = loadpdb %s' %fipdbf, file=lp)

    ##The Disulfur Bond information
    if disul != []:
        for i in disul:
            at1 = i[0]
            at2 = i[1]
            resid1 = mol.atoms[at1].resid
            resid2 = mol.atoms[at2].resid
            atname1 = mol.atoms[at1].atname
            atname2 = mol.atoms[at2].atname
            print('bond', 'mol.' + str(resid1) + '.' + atname1, 'mol.' + \
                  str(resid2) + '.' + atname2, file=lp)

    ##Bond including the metal ions
    if model == 1:
        for bond in blist1:
            if list(set(bond) & set(ionids)) != []:
                at1 = bond[0]
                at2 = bond[1]
                resid1 = mol.atoms[at1].resid
                resid2 = mol.atoms[at2].resid
                atname1 = mol.atoms[at1].atname
                atname2 = mol.atoms[at2].atname
                print('bond', 'mol.' + str(resid1) + '.' + atname1, 'mol.' + \
                      str(resid2) + '.' + atname2, file=lp)

    ##Nonstandard residues with nearby residues

    if model in [1, 2]:
        bondcmds = []
        for i in metcenres1:
            resname = mol0.residues[i].resname
            print('Renamed residues includes: ' + str(i) + '-' + resname)
            if i in reslist0.nterm:
                cmdi = 'bond mol.' + str(i) + '.C' + ' mol.' + str(i+i) + '.N'
                if cmdi not in bondcmds:
                    bondcmds.append(cmdi)
            elif i in reslist0.cterm:
                cmdi = 'bond mol.' + str(i-1) + '.C' + ' mol.' + str(i) + '.N'
                if cmdi not in bondcmds:
                    bondcmds.append(cmdi)
            elif i in reslist0.std:
                cmdi = 'bond mol.' + str(i-1) + '.C' + ' mol.' + str(i) + '.N'
                if cmdi not in bondcmds:
                    bondcmds.append(cmdi)
                cmdi = 'bond mol.' + str(i) + '.C' + ' mol.' + str(i+1) + '.N'
                if cmdi not in bondcmds:
                    bondcmds.append(cmdi)
        for j in bondcmds:
            print(j, file=lp)

    #Save dry structure
    print('savepdb mol %s_dry.pdb' %gname, file=lp)
    print('saveamberparm mol %s_dry.prmtop %s_dry.inpcrd' \
          %(gname, gname), file=lp)
    #Solvatebox
    if watermodel == 'tip3p':
        print('solvatebox mol TIP3PBOX 10.0', file=lp)
    elif watermodel == 'spce':
        print('solvatebox mol SPCBOX 10.0', file=lp)
        print('loadamberparams frcmod.spce', file=lp)
    elif watermodel == 'tip4pew':
        print('solvatebox mol TIP4PEWBOX 10.0', file=lp)
        print('loadamberparams frcmod.tip4pew', file=lp)
    #Add counter ions
    print('addions mol Na+ 0', file=lp)
    print('addions mol Cl- 0', file=lp)
    #Save solvated structure
    print('savepdb mol %s_solv.pdb' %gname, file=lp)
    print('saveamberparm mol %s_solv.prmtop %s_solv.inpcrd' \
          %(gname, gname), file=lp)
    print('quit', file=lp)
    print(' ', file=lp)

    lp.close()

    print('Finish generating the leap input file.')

    #tleap
    #os.system('tleap -s -f %s > %s' %(ileapf, oleapf))
