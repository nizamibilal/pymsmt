#!/usr/bin/python
from __future__ import print_function
import os
import numpy as np
import scipy.stats as stats
import pylab as pl
import itertools
   
#==============================================================================
# function for statistical analysis of Pdbsearcher.py results
#==============================================================================

def do_analysis(geo1, georms1):
    af = open ('analysis.txt', 'w')
    one = Ln2 = Tr3 = Te4 = Sq4 = Tp5 = Sp5 = Tn5 = Oc6 = Bt7 = Bt8 = 0
    Ln2_georms = []
    Tr3_georms = []
    Te4_georms = []
    Sq4_georms = []
    Tp5_georms = []
    Sp5_georms = []
    Tn5_georms = []
    Oc6_georms = []
    Bt7_georms = []
    Bt8_georms = []
    for geo, georms in itertools.izip(geo1, georms1):
        
        if geo == '1':
            one = one+1
            #one_georms.append(georms)
        if geo == '2Ln':
            Ln2 = Ln2+1
            Ln2_georms.append(georms)
            
	
        if geo == '3Tr':
            Tr3 = Tr3+1
            Tr3_georms.append(georms)
	
        if geo == '4Te':
            Te4 = Te4+1
            Te4_georms.append(georms)
        
        if geo == '4Sq':
            Sq4 = Sq4+1
            Sq4_georms.append(georms)
        
        if geo == '5Tp':
            Tp5 = Tp5+1
            Tp5_georms.append(georms)
        
        if geo == '5Sp':
            Sp5 = Sp5+1
            Sp5_georms.append(georms)
        
        if geo == '5Tn':
            Tn5 = Tn5+1
            Tn5_georms.append(georms)
        
        if geo == '6Oc':
            Oc6 = Oc6+1
            Oc6_georms.append(georms)
        
        if geo == '7Bt':
            Bt7 = Bt7+1
            Bt7_georms.append(georms)
	
        if geo == '8Bt':
            Bt8 = Bt8+1
            Bt8_georms.append(georms)  
    
    # write the distribution plots of georms for each geometry types as image files
    
    Ln2_georms = sorted(Ln2_georms)
    ##one_georms = sorted(one_georms) ##no need as georms is always 0
    Tr3_georms = sorted(Tr3_georms)
    Te4_georms = sorted(Te4_georms)
    Sq4_georms = sorted(Sq4_georms)
    Tp5_georms = sorted(Tp5_georms)
    Sp5_georms = sorted(Sp5_georms)
    Tn5_georms = sorted(Tn5_georms)
    Oc6_georms = sorted(Oc6_georms)
    Bt7_georms = sorted(Bt7_georms)
    Bt8_georms = sorted(Bt8_georms)
    

    if len(Ln2_georms) >0:
        #fit = stats.norm.pdf(Ln2_georms, np.mean(Ln2_georms), np.std(Ln2_georms))
        #pl.plot(Ln2_georms,fit,'-o')
        pl.hist(Ln2_georms)
        pl.savefig('distln2.png')

    if len(Tr3_georms) >0: 
        #fit = stats.norm.pdf(Tr3_georms, np.mean(Tr3_georms), np.std(Tr3_georms))
        #pl.plot(Tr3_georms,fit,'-o')
        pl.hist(Tr3_georms)
        pl.savefig('disttr3.png')
        
    if len(Te4_georms) >0:
        #fit = stats.norm.pdf(Te4_georms, np.mean(Te4_georms), np.std(Te4_georms))
        #pl.plot(Te4_georms,fit,'-o')
        pl.hist(Te4_georms,normed=True)
        pl.savefig('distte4.png')
    
    if len(Sq4_georms) >0:
        #fit = stats.norm.pdf(Sq4_georms, np.mean(Sq4_georms), np.std(Sq4_georms))
        #pl.plot(Sq4_georms,fit,'-o')
        pl.hist(Sq4_georms,normed=True)
        pl.savefig('distsq4.png')
    
    if len(Tp5_georms) >0:
        #fit = stats.norm.pdf(Tp5_georms, np.mean(Tp5_georms), np.std(Tp5_georms))
        #pl.plot(Tp5_georms,fit,'-o')
        pl.hist(Tp5_georms,normed=True)
        pl.savefig('disttp5.png')
        
    if len(Sp5_georms) >0:
        #fit = stats.norm.pdf(Sp5_georms, np.mean(Sp5_georms), np.std(Sp5_georms))
        #pl.plot(Sp5_georms,fit,'-o')
        pl.hist(Sp5_georms,normed=True)
        pl.savefig('distsn5.png')
    if len(Tn5_georms) >0:
        #fit = stats.norm.pdf(Tn5_georms, np.mean(Tn5_georms), np.std(Tn5_georms))
        #pl.plot(Tn5_georms,fit,'-o')
        pl.hist(Tn5_georms,normed=True)
        pl.savefig('disttn5.png')
    
    if len(Oc6_georms) >0:
        #fit = stats.norm.pdf(Oc6_georms, np.mean(Oc6_georms), np.std(Oc6_georms))
        #pl.plot(Oc6_georms,fit,'-o')
        pl.hist(Oc6_georms,normed=True)
        pl.savefig('distoc6.png')
    
    if len(Bt7_georms) >0:
        #fit = stats.norm.pdf(Bt7_georms, np.mean(Bt7_georms), np.std(Bt7_georms))
        #pl.plot(Bt7_georms,fit,'-o')
        pl.hist(Bt7_georms,normed=True)
        pl.savefig('distbt7.png')
    
    if len(Bt8_georms) >0:
        #fit = stats.norm.pdf(Bt8_georms, np.mean(Bt8_georms), np.std(Bt8_georms))
        #pl.plot(Bt8_georms,fit,'-o')
        pl.hist(Bt8_georms,normed=True)
        pl.savefig('distbt8.png') 
    #print analysis file
    print ('Geom,', 'one,','Ln2,','Tr3,','Te4,','Sq4,','Tp5,','Sp5,','Tn5,','Oc6,','Bt7,', 'Bt8,', file=af)
    print ('Count', ',',one, ',',Ln2, ',',Tr3, ',',Te4, ',',Sq4, ',',Tp5, ',',Sp5, ',',Tn5, ',',Oc6, ',',Bt7, ',',Bt8, file=af) 
    af.close()
    return;

    
    
def do_stat(geo1, reslets1):
    d5tp = {}
    #d5tp.setdefault(5tp,[])
    af = open ('analysis2.txt', 'w')
    #print ('Geo,', 'sphere,', file=af)
    geo_uniq = set(geo1)
    geo_uniq = list(geo1)
    print (len(geo1))
    reslets_uniq = set(reslets1)
    reslets_uniq = list(reslets1)
    print(len(reslets1))
    for geo, r in itertools.izip(geo1, reslets1):
        print(geo)
        if geo == '5Tp':
            d5tp = {}
            d5tp.setdefault('5tp', []).append(r)
            print(d5tp)
            
                #count = 0
            print(r, file=af)
            #elif geo == '8Bt':
            #    print(geo, ',', file=af)
            #    count = 0
            #    print(r, file=af)
            #elif geo == '1':'
            #    print(geo, ',', file=af)
            #    count = 0
            #    print(r, file=af)
    af.close()
    return;        
        
    
def do_stat1(geo1):
    'count occurance of each type of geometry. results are written to a file'
    one = Ln2 = Tr3 = Te4 = Sq4 = Tp5 = Sp5 = Tn5 = Oc6 = Bt7 = Bt8 = 0
    af = open ('geo_analysis.txt', 'w')
    for geo in geo1:
        if geo == '1':
            one = one+1
        if geo == '2Ln':
            Ln2 = Ln2+1    
        if geo == '3Tr':
            Tr3 = Tr3+1	
        if geo == '4Te':
            Te4 = Te4+1     
        if geo == '4Sq':
            Sq4 = Sq4+1        
        if geo == '5Tp':
            Tp5 = Tp5+1        
        if geo == '5Sp':
            Sp5 = Sp5+1        
        if geo == '5Tn':
            Tn5 = Tn5+1        
        if geo == '6Oc':
            Oc6 = Oc6+1       
        if geo == '7Bt':
            Bt7 = Bt7+1	
        if geo == '8Bt':
            Bt8 = Bt8+1
            
    print ('Geom,', 'one,','Ln2,','Tr3,','Te4,','Sq4,','Tp5,','Sp5,','Tn5,','Oc6,','Bt7,', 'Bt8,', file=af)
    print ('Count', ',',one, ',',Ln2, ',',Tr3, ',',Te4, ',',Sq4, ',',Tp5, ',',Sp5, ',',Tn5, ',',Oc6, ',',Bt7, ',',Bt8, file=af)
    af.close()
    return;    
    