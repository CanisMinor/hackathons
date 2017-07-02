#!/usr/bin/env python3
import sys
import os
import pickle

pp=1
if (pp):
    def ppr(*x):
        print(" ".join(map(str,x)))
else:
    def ppr(*x):
        pass

files = []

def M():
    if len(sys.argv)<2:
        print("Usage:\n./filer.py <Directory Name>")
        return
    filedir = sys.argv[1]
    outname = filedir + ".pickle"
    if len(sys.argv)>=3:
        outname = sys.argv[2]

    with open(outname,"rb") as f:
        files = pickle.load(f)

    for f in files:
        for t in f:
            print(t,f[t])
        print()
    


M()
