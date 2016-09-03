#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys


lines = open (sys.argv[1], "rb").readlines ()

table = {}
for l in lines[1:]:
    (process, version, total, distinct) = l.split (',')
    process = process.strip()
    version = version.strip()
    try:
        total = int(total.strip())
    except:
        total = "NA"
    try:
        distinct = int(distinct.strip())
    except:
        distinct = "NA"

    if process in table.keys ():
        table[process].update({version:{"total" : total, "distinct" : distinct}})
    else:
        table[process] = {version:{"total" : total, "distinct" : distinct}}


processes = table.keys()
versions = []
for process in table.keys():
    vercrashes = table[process]
    for v in vercrashes.keys():
        if v not in versions:
            versions.append(v)

# print top row - versions
print ",",
for v in versions:
    print ("%s,," % (v)),
print

print ",",
for v in versions:
    print ("Total Crashes, Distinct Devices,"),
print

for p in processes:
    print "%s," % (p),
    for v in versions:
        try:
            print "%s," % (table[p][v]['total']),
        except:
            print ",",

        try:
            print "%s," % (table[p][v]['distinct']),
        except:
            print ",",
    print

for i in range (5):
    print

print "Crashes Per Device"
print ",",
for v in versions:
    print ("%s," % (v)),
print

for p in processes:
    print "%s," % (p),
    for v in versions:
        try:
            if table[p][v]['distinct'] != 'NA' and table [p][v]['total'] != 'NA':
                print "%.2f," % (table[p][v]['total']/(1.0 * table[p][v]['distinct'])),
            else:
                print ",",
        except:
            print ",",
    print
