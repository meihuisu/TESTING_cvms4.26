#!/usr/bin/env python


## chop up BILLY's data into one csv per target loc

import sys
import os
import json
import csv
import pdb

DATA_STUB="BILLY_DATA/S426_Profiles_20200210"

LOC_POINTS=15
VSFILE = DATA_STUB+"_vs.csv"
VPFILE = DATA_STUB+"_vp.csv"

## started with index of 0
LIST_SZ=LOC_POINTS+1
OUTLINES_LIST=[0]*LIST_SZ
OUTLABEL_LIST=[0]*LIST_SZ
OUTIDX_LIST=[0]*LIST_SZ
OUTFILE_LIST=[0]*LIST_SZ
OUTFP_LIST=[0]*LIST_SZ

def process(aType) :
  
  fname=VPFILE
  if (aType=='vs') :
    fname=VSFILE
  vslines=[]

## first row is label
  with open(fname) as csvfile:
     reader = csv.DictReader(csvfile)
     first=True
     for row in reader:
         if (first) :
             first=False
             keys=row.keys()
             for key in keys :
               try:
                  ikey=int(key)
                  vstr=row[key].replace(" ","_")
                  outfname=vstr+"_Billy_25_"+aType+".csv"
                  OUTLINES_LIST[ikey]=[]
                  OUTLABEL_LIST[ikey]=row[key]
                  OUTFILE_LIST[int(key)]=outfname
                  outfp=open(outfname,"w+")
                  OUTFP_LIST[ikey]=outfp
                  outfp.write("BILLY-25\n")
               except ValueError:
                  pass
         else :
             keys=row.keys()
             for key in keys :
               try:
                  ikey=int(key)  
                  OUTLINES_LIST[ikey].append(row[key])
               except ValueError:
                  pass

    ## reverse and output
     idx=1
     while idx < LIST_SZ :
        line=OUTLINES_LIST[idx]
        line.reverse()
        fp=OUTFP_LIST[idx]
        for term in line:
          fp.write(term)
          fp.write("\n")
        fp.close()
        idx += 1

#### MAIN ###
process("vs")
process("vp")

