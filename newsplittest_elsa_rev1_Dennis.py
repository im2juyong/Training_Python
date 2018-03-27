import sys
import string
import re

import numpy as np
import pandas as pd

datafn = "C:/Users/Dennis/Desktop/PT/DLG_WN17B636_S01_05_PT1_20180315123237.txt"

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

line_num = 0

wns = []
Map = {}
tnames = []

TData={}
TDatas={}

line_num = 0

site={}
i=0
j=0

for line in dataf:
    line_num += 1
    line = line.strip()
    if not line: continue  # blank line

    if re.search("\s+PASS\s+", line) or re.search("\s+FAIL\s+", line) :
        ls = line.split()

        if len(ls) < 11: continue

        site = int(ls[1])
        tname = ls[3]

        if "OS_" in tname: continue
        if "LKG_" in tname: continue

        if tname not in tnames : tnames.append(tname)

        index = 7

        if ls[index].isalpha(): index += 1

        v = ls[index]
        if "N" in v: continue
        index += 1
        v = float(v)
        if ls[index].isalpha():
            v *= UPrefix[ls[index][0]]
        TData[site,tname]=v

        continue

    if re.search("Temp\s*:", line):
        tline = line.replace('C',' ')
        tls   = tline.split()
        temp  = float(tls[2])



    if "=====" in line:
        yx={}
        while True:
            try : line = dataf.next()
            except : break

            if "Illuminator" in line : line = dataf.next()
            if "Site:" not in line : break

            ls = line.strip().split()
            bin = int(ls[3])

            if not bin : continue

            site = int(ls[1])
            x = int(ls[-3])
            y = int(ls[-1][:-1])
            yx[site] = y,x
            print(yx[site])

            Map[wn][y, x] = site, bin, temp

        for (s,t),v in TData.items():
            #TDatas[wn][yx[s],t]=v
            print(TData.items())


    if "Wafer ID" in line:
        wn = int(line.split()[-1])
        print (wn)
        if wn not in wns : wns.append(wn)
        TDatas[wn] = {}
        Map[wn]={}
        continue
