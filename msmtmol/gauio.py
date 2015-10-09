"""
Module for writting a Gaussian file and read the coordinates and force
constants from Gaussian output file.
"""
from __future__ import absolute_import, print_function, division
import numpy
import linecache
from pymsmtexp import *
from msmtmol.constants import B_TO_A
from msmtmol.pt import AtomicNum

#------------------------------------------------------------------------------
#------------------------Write Gaussian input file-----------------------------
#------------------------------------------------------------------------------

def write_gauatm(gauatm, fname, signum=3):
    wf = open(fname, 'a')
    if signum == 3:
        print("%-6s   %8.3f %8.3f %8.3f" %(gauatm.element, \
                     gauatm.crdx, gauatm.crdy, gauatm.crdz), file=wf)
    elif signum == 4:
        print("%-6s   %9.4f %9.4f %9.4f" %(gauatm.element, \
                     gauatm.crdx, gauatm.crdy, gauatm.crdz), file=wf)
    wf.close()

def write_gauatm_opth(gauatm, fname, signum=3):
    wf = open(fname, 'a')
    if gauatm.element == "H":
        print("%-6s  0 %8.3f %8.3f %8.3f" %(gauatm.element, \
            gauatm.crdx, gauatm.crdy, gauatm.crdz), file=wf)
    else:
        print("%-6s -1 %8.3f %8.3f %8.3f" %(gauatm.element, \
            gauatm.crdx, gauatm.crdy, gauatm.crdz), file=wf)
    wf.close()

def write_sdd_basis(gatms, gauf):

    atnames = [i.element for i in gatms]
    atnames = list(set(atnames))
    atnums = [AtomicNum[i] for i in atnames]

    w_gauf = open(gauf, 'a')
    print(" ", file=w_gauf)
    for i in atnames:
        if AtomicNum[i] <= 18:
            print(i, end=' ', file=w_gauf)
    print("0", file=w_gauf)
    print("6-31G*", file=w_gauf)
    print("****", file=w_gauf)

    for i in atnames:
        if Atomic_Num[i] >= 19:
            print(i, file=w_gauf)
    print("0", file=w_gauf)
    print("SDD", file=w_gauf)
    print("****", file=w_gauf)
    print(" ", file=w_gauf)

    for i in atnames:
        if Atomic_Num[i] >= 19:
            print(i, file=w_gauf)
    print("0", file=w_gauf)
    print("SDD", file=w_gauf)
    print("****", file=w_gauf)
    w_gauf.close()

def write_gau_optf(outf, goptf, smchg, SpinNum, gatms, signum=3):

    ##Geometry Optimization file
    optf = open(goptf, 'w')
    print("$RunGauss", file=optf)
    print("%%Chk=%s_small_opt.chk" %outf, file=optf)
    print("%Mem=3000MB", file=optf)
    print("%NProcShared=2", file=optf)
    print("#N B3LYP/6-31G* Geom=PrintInputOrient " + \
                   "Integral=(Grid=UltraFine) Opt", file=optf)
    print("SCF=XQC", file=optf)
    print(" ", file=optf)
    print("CLR", file=optf)
    print(" ", file=optf)
    print("%d  %d" %(smchg, SpinNum), file=optf)
    optf.close()

    if signum == 3:
        for gatmi in gatms:
            write_gauatm(gatmi, goptf)
    elif signum == 4:
        for gatmi in gatms:
            write_gauatm(gatmi, goptf, 4)

    ##Geometry Optimization file
    optf = open(goptf, 'a')
    print(" ", file=optf)
    print(" ", file=optf)
    optf.close()

def write_gau_fcf(outf, gfcf):

    ##Force constant calculation file
    fcf = open(gfcf, 'w')
    print("$RunGauss", file=fcf)
    print("%%Chk=%s_small_opt.chk" %outf, file=fcf)
    print("%Mem=3000MB", file=fcf)
    print("%NProcShared=2", file=fcf)
    print("#N B3LYP/6-31G* Freq=NoRaman Geom=AllCheckpoint Guess=Read", file=fcf)
    print("Integral=(Grid=UltraFine) SCF=XQC IOp(7/33=1)", file=fcf)
    print(" ", file=fcf)
    print(" ", file=fcf)
    fcf.close()

def write_gau_mkf(outf, gmkf, lgchg, SpinNum, gatms, ionnames, chargedict,
                  IonLJParaDict, largeopt, signum=3):

    ##MK RESP input file
    mkf = open(gmkf, 'w')
    print("$RunGauss", file=mkf)
    print("%%Chk=%s_large_mk.chk" %outf, file=mkf)
    print("%Mem=3000MB", file=mkf)
    print("%NProcShared=2", file=mkf)

    if largeopt == 0:
        print("#N B3LYP/6-31G* Integral=(Grid=UltraFine) " + \
                      "Pop(MK,ReadRadii) SCF=XQC", file=mkf)
    elif largeopt in [1, 2]:
        print("#N B3LYP/6-31G* Integral=(Grid=UltraFine) Opt " + \
                      "Pop(MK,ReadRadii) SCF=XQC", file=mkf)

    print("IOp(6/33=2)", file=mkf)
    print(" ", file=mkf)
    print("CLR", file=mkf)
    print(" ", file=mkf)
    print("%d  %d" %(lgchg, SpinNum), file=mkf)
    mkf.close()

    #For Gaussian file
    if signum == 3:
        if largeopt in [0, 2]:
            for gatmi in gatms:
                write_gauatm(gatmi, gmkf)
        elif largeopt == 1:
            for gatmi in gatms:
                write_gauatm_opth(gatmi, gmkf)
    elif signum == 4:
        if largeopt in [0, 2]:
            for gatmi in gatms:
                write_gauatm(gatmi, gmkf, signum)
        elif largeopt == 1:
            for gatmi in gatms:
                write_gauatm_opth(gatmi, gmkf, signum)

    ##print the ion radius for resp charge fitting in MK RESP input file
    mkf = open(gmkf, 'a')
    print(" ", file=mkf)

    for ionname in ionnames:
        chg = int(round(chargedict[ionname], 0))
        if len(ionname) > 1:
            ionname = ionname[0] + ionname[1:].lower()
        for i in range(0, chg):
            fchg = chg - i
            if ionname+str(fchg) in list(IonLJParaDict.keys()):
                if i != 0:
                    print("Could not find VDW radius for element %s with charge "
                          "+%d, use the one of charge +%d" %(ionname, chg, fchg))
                vdwradius = IonLJParaDict[ionname + str(fchg)][0]
                break
        if vdwradius is None:
            raise pymsmtError("Could not find VDW parameters/radius for "
                              "element %s with charge +%d" %(ionname, chg))
        print(ionname, vdwradius, file=mkf)
    print(" ", file=mkf)

    if largeopt in [1, 2]:
        for ionname in ionnames:
            chg = int(round(chargedict[ionname], 0))
            if len(ionname) > 1:
                ionname = ionname[0] + ionname[1:].lower()
            for i in range(0, chg):
                fchg = chg - i
                if ionname+str(fchg) in list(IonLJParaDict.keys()):
                    if i != 0:
                        print("Could not find VDW radius for element %s with charge "
                              "+%d, use the one of charge +%d" %(ionname, chg, fchg))
                    vdwradius = IonLJParaDict[ionname + str(fchg)][0]
                    break
            if vdwradius is None:
                raise pymsmtError("Could not find VDW parameters/radius "
                                  "for element %s with %d charge" %(ionname, chg))
            print(ionname, vdwradius, file=mkf)
        print(" ", file=mkf)
        print(" ", file=mkf)

    if largeopt == 0:
        print(" ", file=mkf)

    mkf.close()

#------------------------------------------------------------------------------
#-----------------------Read info from Gaussian output file--------------------
#------------------------------------------------------------------------------

def get_crds_from_fchk(fname, atnums):

    #fchk file uses Bohr unit
    crds = []

    crdnums = atnums * 3
    fp = open(fname, 'r')
    i = 1
    for line in fp:
        if 'Current cartesian coordinates' in line:
            beginl = i + 1
            line = line.strip('\n')
            line = line.split()
            crdnums2 = int(line[-1])
        i = i + 1
    fp.close()

    if crdnums == crdnums2:
        pass
    else:
        raise pymsmtError('The coordinates number in fchk file are not consistent '
                         'with the atom number.')

    if crdnums%5 == 0:
        endl = crdnums//5 + beginl - 1
    else:
        endl = crdnums//5 + beginl

    for i in range(beginl, endl+1):
        line = linecache.getline(fname, i)
        line = line.strip('\n')
        crd = line.split()
        for j in crd:
            if j != ' ':
                crds.append(float(j))

    linecache.clearcache()
    return crds

def get_matrix_from_fchk(fname, msize):

    crds = []

    elenums = msize * (msize + 1)
    elenums = elenums//2

    fp = open(fname, 'r')
    i = 1
    for line in fp:
        if 'Cartesian Force Constants' in line:
            beginl = i + 1
            line = line.strip('\n')
            line = line.split()
            elenums2 = int(line[-1])
        i = i + 1
    fp.close()

    if elenums == elenums2:
        pass
    else:
        raise pymsmtError('The atom number is not consistent with the'
                         'matrix size in fchk file.')

    if elenums%5 == 0:
        endl = beginl + elenums//5 - 1
    else:
        endl = beginl + elenums//5

    fcmatrix = numpy.array([[float(0) for x in range(msize)] for x in range(msize)])

    for i in range(beginl, endl+1):
        line = linecache.getline(fname, i)
        line = line.strip('\n')
        crd = line.split()
        for j in crd:
            if j != ' ':
                crds.append(float(j))

    i = 0
    for j in range(0, msize):
        for k in range(0, j+1):
            fcmatrix[j][k] = crds[i]
            fcmatrix[k][j] = crds[i]
            i = i + 1

    linecache.clearcache()
    return fcmatrix

def get_crds_from_log(logfname, g0x):

    #Log file uses angs. as unit

    if g0x == 'g03':
        fp = open(logfname)
        ln = 1
        for line in fp:
            if 'Redundant internal coordinates' in line:
                bln = ln + 3
            elif 'Recover connectivity data from disk' in line:
                eln = ln - 1
            ln = ln + 1
        fp.close()
    elif g0x == 'g09':
        fp = open(logfname)
        ln = 1
        for line in fp:
            if 'Redundant internal coordinates' in line:
                bln = ln + 1
            elif 'Recover connectivity data from disk' in line:
                eln = ln - 1
            ln = ln + 1
        fp.close()

    crds = []
    ln = 1
    fp1 = open(logfname)
    for line in fp1:
        if (ln >= bln) and (ln <= eln):
            line = line.strip('\n')
            line = line.split(',')
            line = line[-3:]
            line = [float(i) for i in line]
            crds += line
        ln = ln + 1
    fp1.close()

    return crds

def get_fc_from_log(logfname):

    stringle = 'calculate D2E/DX2 analytically'
    stringfc = ' Internal force constants:'

    sturefs = []
    vals = []

    ##Get the values for each bond, angle and dihedral
    fp = open(logfname, 'r')
    for line in fp:
        if stringle in line:
            line = line.strip('\n')
            line = line.strip('!')
            line = line.lstrip(' !')
            line = line.split()
            val = float(line[2])
            vals.append(val)
            typ = line[0][0]

            line[1] = line[1].lstrip(typ)
            line[1] = line[1].lstrip('L')
            line[1] = line[1].lstrip('(')
            line[1] = line[1].rstrip(')')

            ats = line[1].split(',')
            ats = [int(i) for i in ats]
            sturefs.append(tuple(ats))
    fp.close()

    maxnum = len(sturefs)

    ##Get the force constant begin line
    fp = open(logfname, 'r')
    lnum = 1
    for line in fp:
        if stringfc in line:
            blnum = lnum + 2
        lnum = lnum + 1
    fp.close()

    blnum1 = blnum

    ##Get the line number list to read the force constant
    numl = []

    if (maxnum%5 != 0):
        for i in range(0, int(maxnum//5)+1):
            gap = maxnum - len(numl) + 1
            for j in range(0, 5):
                if len(numl) < maxnum:
                    numl.append(blnum1 + j)
            blnum1 = blnum1 + gap
    else:
        for i in range(0, int(maxnum//5)):
            gap = maxnum - len(numl) + 1
            for j in range(0, 5):
                if len(numl) < maxnum:
                    numl.append(blnum1 + j)
            blnum1 = blnum1 + gap

    fcs = []
    fp = open(logfname, 'r')
    lnum = 1
    for line in fp:
        if lnum in numl:
            line = line.strip('\n')
            line = line.split()
            numv = len(line)
            fc = float(line[-1].replace('D', 'e'))
            fcs.append(fc)
        lnum = lnum + 1
    fp.close()

    ##Return three lists: identifications, values, force constants
    return sturefs, vals, fcs

def get_esp_from_gau(logfile, espfile):
    #Gaussian log file uses Angstrom as unit, esp file uses Bohr

    #------------Coordinate List for the Atom and ESP Center--------------
    crdl1 = []
    crdl2 = []

    ln = 1
    fp = open(logfile, 'r')
    for line in fp:
        if 'Electrostatic Properties Using The SCF Density' in line:
            bln = ln
        ln = ln + 1
    fp.close()

    ln = 1
    fp = open(logfile, 'r')
    for line in fp:
        if ln >= bln:
            if '      Atomic Center' in line:
                #line = line.strip('\n')
                #line = line.split()
                crd = (float(line[32:42])/B_TO_A, float(line[42:52])/B_TO_A, float(line[52:62])/B_TO_A)
                crdl1.append(crd)
            elif ('     ESP Fit Center' in line):
                #line = line.strip('\n')
                #line = line.split()
                crd = (float(line[32:42])/B_TO_A, float(line[42:52])/B_TO_A, float(line[52:62])/B_TO_A)
                crdl2.append(crd)
        ln = ln + 1
    fp.close()

    #------------ESP values for Atom and ESP Center--------------------
    #Both log and esp files use Atomic Unit Charge

    espl1 = []
    espl2 = []

    ln = 1
    fp = open(logfile, 'r')
    for line in fp:
        if 'Electrostatic Properties (Atomic Units)' in line:
            bln = ln + 6
        ln = ln + 1
    fp.close()

    ln = 1
    fp = open(logfile, 'r')
    for line in fp:
        if ln >= bln:
            if ' Atom ' in line:
                line = line.strip('\n')
                line = line.split()
                esp = float(line[-1])
                espl1.append(esp)
            elif (' Fit ' in line):
                line = line.strip('\n')
                line = line.split()
                esp = float(line[-1])
                espl2.append(esp)
        ln = ln + 1
    fp.close()

    #----------------Check and print-----------------------
    if (len(crdl1) == len(espl1)) and (len(crdl2) == len(espl2)):
        w_espf = open(espfile, 'w')
        print("%5d%5d%5d" %(len(crdl1), len(crdl2), 0), file=w_espf)
        for i in range(0, len(crdl1)):
            crd = crdl1[i]
            print("%16s %15.7E %15.7E %15.7E" %(' ', crd[0], crd[1], crd[2]), file=w_espf)
        for i in range(0, len(crdl2)):
            crd = crdl2[i]
            esp = espl2[i]
            print("%16.7E %15.7E %15.7E %15.7E" %(esp, crd[0], crd[1], crd[2]), file=w_espf)
        w_espf.close()
    else:
        raise pymsmtError("The length of coordinates and ESP charges are different!")
