#!/usr/bin/env python3
import sys
import os
import pickle
import subprocess
import dateutil.parser as dp
import datetime as dt
import textract as tx

from convertbng.util import convert_bng, convert_lonlat

pp=1
if (pp):
    def ppr(*x):
        print(" ".join(map(str,x)))
else:
    def ppr(*x):
        pass

def M():
    if (len(sys.argv)<2):
        return
    with open(sys.argv[1], "r") as f:
        places = {}
        validtypes = {"city":"c","town":"t","village":"v"}
        for l in f:
            x = l.strip().split(',')
            otype = x[7].lower()
            if otype not in validtypes:
                continue
            ot = validtypes[otype]
#            name = (x[2]+x[4]).lower()
            name = (x[2]+x[4]) # keep upper/lower for place names
            gbx = float(x[8])
            gby = float(x[9])
            ll = convert_lonlat([gbx],[gby])
            lon = ll[0][0]
            lat = ll[1][0]
            #            print(",".join([name,otype,str(lat),str(lon)]))
            places[name]=(ot,lat,lon)
    with open("bigdat.pickle","wb") as g:
        pickle.dump(places,g)

M()
