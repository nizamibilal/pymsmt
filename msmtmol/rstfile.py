"""
This module is used for reading the rst file.
"""
import numpy

def read_rstf(fname):

    fp = open(fname, 'r')
    Vp = []
    crds = []

    num = 1
    #Read the rst file
    for line in fp:
        if num >= 2:
            line = line.strip('\n')
            line = line.split()
            vals = []
        
            #get pure list
            for i in line:
                if i != '' and i != ' ':
                    vals.append(i)

            if len(vals) <= 2: #it is a atom number line
                try:
                    atnum = int(vals[0])
                except:
                    continue
            elif len(vals) >= 3: #it is coordinate line
                for i in vals:
                    crds.append(i)

        num = num + 1

    #Re-arrange the data
    crds = [float(i) for i in crds]
    crds = crds[0:3*atnum] #the coordinates
    boxs = crds[3*atnum:] #the last several values

    for i in range(0, atnum):
        Vp.append(numpy.array(crds[3*i:3*i+3]))
    V = numpy.array(Vp)
    return V
