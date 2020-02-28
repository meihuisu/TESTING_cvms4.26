#!/usr/bin/env python

import os
import sys
import pdb
from subprocess import call, Popen, PIPE, STDOUT

from variables import loc_list, slice_list

DEBUG=0
DELTA=25

##  EnJui's format
##   1    1  -116.00000   30.44987      0.000 5473.802 3162.570 2729.205
##   1    1  -116.00000   30.44987 -49500.000 7917.237 4570.960 3115.128
##  po's format 
##   1    1  3.0449868e+01  -1.1600000e+02   0.0000000e+00   3.1625701e+00   5.4738018e+00
##   1    1  3.0449868e+01  -1.1600000e+02   4.9500000e+01   4.5709600e+00   7.9172368e+00
NOTPO=1

## MODEL dataset Phil found in EnJui's directory
##   DATA_STUB="ASCII_MODEL_DATA/CVM4SI26_slices/CVM4SI26_slice_"
## MODEL dataset Phil downloaded from PO's website
##   DATA_STUB="PO_DATA/PO_CVM4SI26_slice_"

if NOTPO:
  DATA_STUB="ASCII_MODEL_DATA/CVM4SI26_slices/CVM4SI26_slice_"
  MODEL_STUB="_model_"
  UCVM_STUB="_ucvm_"
  MODEL_HEADER_STUB="MODEL-"
  UCVM_HEADER_STUB="UCVM-"
else:
  DATA_STUB="PO_DATA/PO_CVM4SI26_slice_"
  MODEL_STUB="_po_model_"
  UCVM_STUB="_po_ucvm_"
  MODEL_HEADER_STUB="PO-MODEL-"
  UCVM_HEADER_STUB="PO-UCVM-"

line_offset = []
log_fp=0
file_fp=0
latlon_fp=0
model_vs_fp=0
model_vp_fp=0
model_result_fp=0
ucvm_result_fp=0
ucvm_vs_fp=0
ucvm_vp_fp=0

track_vs=0
track_vp=0
track_rho=0
track_count=0
ucvm_track_vs=0
ucvm_track_vp=0
ucvm_track_rho=0
pnts=""

## build offset cache first
def processIt(file) :
  offset = 0
  for line in file:
    line_offset.append(offset)
    offset += len(line)
  file.seek(0)

# Now, to skip to line n (with the first line being line 0), just do
def lookup(n):
  file_fp.seek(line_offset[n-1])
  line=file_fp.readline()
  if DEBUG:
      log_fp.write(line)
  return line


## 
def addToUCVM(lat,lon,depth) :
  global pnts
  pnts += "%.5f %.5f %.5f\n" % (lon, lat, depth)

def processItUCVM() :
  global ucvm_track_vs
  global ucvm_track_vp
  global ucvm_track_rho

  proc = Popen(["/usr/local/opt/ucvm/bin/run_ucvm_query.sh", "-f", "/usr/local/opt/ucvm/conf/ucvm.conf", "-m", "cvms5" ], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
  output = proc.communicate(input=pnts)[0]
  s=output.split('\n')
  skip=1
  for line in s: 
    if skip or len(line)==0 :
      skip=0
    else:
#      pdb.set_trace()
      ss=line.split()
      if DEBUG:
          log_fp.write(line)
      vvs=float(ss[15])
      vvp=float(ss[14])
      vrho=float(ss[16])

      ucvm_track_vs=ucvm_track_vs+vvs
      ucvm_track_vp=ucvm_track_vp+vvp
      ucvm_track_rho=ucvm_track_rho+vrho

def init_set_result() :
   msg="{ \"matprops\": [\n"
   model_result_fp.write(msg)
   ucvm_result_fp.write(msg)

def init_set() :
   global pnts
   global track_vs
   global track_vp
   global grack_rho
   global track_count
   global ucvm_track_vs
   global ucvm_track_vp
   global ucvm_track_rho
   
   track_vs=0
   track_vp=0
   track_rho=0
   track_count=0
   ucvm_track_vs=0
   ucvm_track_vp=0
   ucvm_track_rho=0
   pnts=""

def add_to_set(line) :
   global track_count
   global track_vs
   global track_vp
   global track_rho
   global ucvm_track_vs
   global ucvm_track_vp
   global ucvm_track_rho
   global pnts

   track_count = track_count + 1
   s=line.split()

   if NOTPO:
     lon=s[2]
     lat=s[3]
     depth=float(s[4]) * -1
   else:
     lon=s[3]
     lat=s[2]
     depth=float(s[4]) * 1000 

   if DEBUG:
       latlon_fp.write(lon+" "+lat+" "+str(depth))

   if NOTPO:
     track_vp=track_vp+float(s[5])
     track_vs=track_vs+float(s[6])
     track_rho=track_rho+float(s[7])
   else:
     track_vp=track_vp+float(s[6]) * 1000
     track_vs=track_vs+float(s[5]) * 1000

   if DEBUG:
       latlon_fp.write("\n")
   ### collect the pnts 
   addToUCVM(float(lat),float(lon),float(depth))

def done_set() :
   track_vs_done=track_vs/track_count
   track_vp_done=track_vp/track_count
   track_rho_done=track_rho/track_count
   processItUCVM()
   ucvm_track_vs_done=ucvm_track_vs/track_count
   ucvm_track_vp_done=ucvm_track_vp/track_count
   ucvm_track_rho_done=ucvm_track_rho/track_count

   if DEBUG:
       msg="final tracking vs"+str(track_vs_done)+" ucvm vs"+str(ucvm_track_vs_done)
       log_fp.write(msg)
       log_fp.write("\n")
       msg="               vp"+str(track_vp_done)+" ucvm vp"+str(ucvm_track_vp_done)
       log_fp.write(msg)
       log_fp.write("\n")
       msg="               rho"+str(track_rho_done)+" ucvm rho"+str(ucvm_track_rho_done)
       log_fp.write(msg)
       log_fp.write("\n")

   ###
   msg="{ \"vs\":"+str(track_vs_done)+",\"vp\":"+str(track_vp_done)+",\"density\":"+str(track_rho_done)+"}"
   model_result_fp.write(msg)
   model_vs_fp.write(str(track_vs_done)+"\n")
   model_vp_fp.write(str(track_vp_done)+"\n")

   msg="{ \"vs\":"+str(ucvm_track_vs_done)+",\"vp\":"+str(ucvm_track_vp_done)+",\"density\":"+str(ucvm_track_rho_done)+"}"
   ucvm_result_fp.write(msg)
   ucvm_vs_fp.write(str(ucvm_track_vs_done)+"\n")
   ucvm_vp_fp.write(str(ucvm_track_vp_done)+"\n")

def close_set_result() :
   msg="]}\n"
   model_result_fp.write(msg)
   ucvm_result_fp.write(msg)

##                 @
##                 ^
##               deltaY
##                 V
##    @<-deltaX->TARGET<-deltaX->@
##               deltaY
##                 V
##                 @


def findLoc(x,y) :
  dx=31
  dy=1536
  nblock = x / dx
  v= (dx * dy) * nblock 
  nstart= (nblock * 31) +1  
  m= (y-1) * 31
  nn= (x-nstart+1)
  nend=m+nn
  vv = v + nend
  if DEBUG:
      msg= "loc>> "+str(x)+","+str(y)+" at "+str(vv)
      log_fp.write(msg)
      log_fp.write("\n")
  return lookup(vv)

def getLocSet(x,y,delta,slice) :
    if DEBUG:
        log_fp.write("=====")
        msg= "for slice"+slice+" (x,y)"+str(x)+","+str(y)+" delta "+str(delta)
        log_fp.write(msg)
        log_fp.write("\n")
    xy_list=[]
    x_start= (x-delta)
    x_end= (x+delta)+1
    y_start=y-delta
    y_end=(y+delta)+1

    init_set()
    for ycoord in xrange(y_start, y_end):
        for xcoord in xrange(x_start, x_end):
           xy_list.append({'x':xcoord,'y':ycoord});
           line = findLoc(xcoord,ycoord)
           add_to_set(line)
    done_set()

#    print len(xy_list)
#    print xy_list

#### MAIN ####


for LOC in loc_list:
   print LOC

   idx=LOC['idx']
   x=int(LOC['x'])
   y=int(LOC['y'])
   loc=LOC['loc']
   locstr="RESULT/"+loc.replace(" ","_");

   if DEBUG:
     log_fp=open(locstr+MODEL_STUB+"log","w+")
     latlon_fp=open(locstr+MODEL_STUB+"latlon","w+")

   model_result_fp=open(locstr+MODEL_STUB+"result.json","w+")
   ucvm_result_fp=open(locstr+UCVM_STUB+"result.json","w+")
   model_vs_fp=open(locstr+MODEL_STUB+str(DELTA)+"_vs.csv","w+")
   model_vp_fp=open(locstr+MODEL_STUB+str(DELTA)+"_vp.csv","w+")
   ucvm_vs_fp=open(locstr+UCVM_STUB+str(DELTA)+"_vs.csv","w+")
   ucvm_vp_fp=open(locstr+UCVM_STUB+str(DELTA)+"_vp.csv","w+")

   model_vs_fp.write(MODEL_HEADER_STUB+str(DELTA)+"\n")
   model_vp_fp.write(MODEL_HEADER_STUB+str(DELTA)+"\n")
   ucvm_vs_fp.write(UCVM_HEADER_STUB+str(DELTA)+"\n")
   ucvm_vp_fp.write(UCVM_HEADER_STUB+str(DELTA)+"\n")

   init_set_result()

   for slice in reversed(slice_list) :
       infile=DATA_STUB+slice
       with open(infile) as f:
          file_fp=f
          processIt(f)
          getLocSet(x,y,DELTA,slice)
       f.close()
       if(slice != "001") :
          ucvm_result_fp.write(",\n")
          model_result_fp.write(",\n")
       else:
          ucvm_result_fp.write("\n")
          model_result_fp.write("\n")

   close_set_result()
   if DEBUG:
       log_fp.close()
       latlon_fp.close()

   model_result_fp.close()
   ucvm_result_fp.close()
   ucvm_vs_fp.close()
   ucvm_vp_fp.close()
   model_vs_fp.close()
   model_vp_fp.close()

