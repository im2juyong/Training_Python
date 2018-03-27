#!/usr/bin/python

import sys
import string
import re


if len(sys.argv) != 2:
    sys.exit("Usage: %s Datalog.txt" % sys.argv[0])

datafn = sys.argv[1]

try: dataf = open(datafn)
except IOError: sys.exit('Cannot Open %s!' % datafn)

UPrefix = {  # unit prefix
 "M": 1e6,
 "k": 1e3,
 "K": 1e3,
 "m": 1e-3,
 "u": 1e-6,
 "n": 1e-9,
 "p": 1e-12,
 "f": 1e-15,
 "V": 1,
 "A": 1,
}

wns = []
Map = {}
tnames = []
TDatas = {}

TData = {}

line_num = 0

for line in dataf:
 line_num += 1
 line = line.strip()
 if not line: continue  # blank line

 #if "PASS" in line or "FAIL" in line:
 if re.search("\s+PASS\s+", line) or re.search("\s+FAIL\s+", line) :
  ls = line.split()
  if len(ls) < 11: continue

  site = int(ls[1])
  tname = ls[3]
  if "OS_" in tname: continue
  if "LKG_" in tname: continue

  if tname not in tnames: tnames.append(tname)

  index = 7
  if ls[index].isalpha(): index += 1

  v = ls[index]
  if "N" in v: continue
  index += 1
  v = float(v)
  if ls[index].isalpha():
   v *= UPrefix[ls[index][0]]
   #if len(ls[index]) == 2 :
   # v *= UPrefix[ls[index][0]]
  TData[site, tname] = v

  continue

 if re.search("Temp\s*:", line) :
    tline = line.replace('C', ' ')
    tls   = tline.split()
    temp  =  float(tls[2])

 if "=====" in line:
  yx = {}
  while True:
   try: line = dataf.next()
   except: break
   if "Illuminator" in line : line = dataf.next()
   if "Site:" not in line: break
   ls = line.strip().split()
   bin = int(ls[3])
   if not bin: continue
   site = int(ls[1])
   x = int(ls[-3])
   y = int(ls[-1][:-1])
   yx[site] = y, x
   Map[wn][y, x] = site, bin, temp
  for (s, t), v in TData.items():
      TDatas[wn][yx[s], t] = v
  if "Device#" in line: TData = {}
  continue

 if re.search("Device#\s*:", line) :
  TData = {}
  continue

 if "Lot ID" in line:
  lot = line.split()[-1]
  print ("test %s",lot)
  #print lot,
  continue

 if "Wafer ID" in line:
  wn = int(line.split()[-1])
  print (wn)
  if wn not in wns: wns.append(wn)
  TDatas[wn] = {}
  Map[wn] = {}
  continue

dataf.close()

import os
csvfn = os.path.splitext(datafn)[0] + ".csv"
try: csvf = open(csvfn, "w")
except: sys.exit("Cannot Create %s" % csvfn)

csvf.write("Lot,Wafer,X,Y,temp,Site,Bin,Split")
for tname in tnames: csvf.write(",%s" % tname)
csvf.write("\n")

split = [
 [  1,  1,  1, ],
 [  1,  1,  1, ],
 [  1,  1,  1, ],
 [  1,  1,  2, ],
]
ysize = len(split)
xsize = len(split[0])

for wn in wns:
 for y, x in sorted(Map[wn].keys()):
  site, bin , temp = Map[wn][y, x]
  csvf.write("%s,#%02d,%d,%d,%4.2f,%d,%d" % (lot, wn, x, y, temp, site, bin))
  csvf.write(",%d" % (split[(y - 11 + 0) % ysize][(x - 11 - 1) % xsize]))
  for tname in tnames: csvf.write(",%s" % TDatas[wn].get(((y, x), tname), ""))
  csvf.write("\n")
csvf.close()
