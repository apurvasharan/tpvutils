#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os

for line in open ('watchdogs.txt').readlines():
    line = line.strip()
    if len(line) != 0:
        match = re.search ('(?P<path>.*)/(?P<boot>Boot_0\d+)/.*', line)

        boot = match.group ('boot')
        num = re.search ('Boot_(?P<num>\d\d\d\d)', boot).group ('num')
        num = int (num)
        newboot = 'Boot_%04d' % (num - 1)

        orgpath = match.group ('path') + "/" + boot + "/" + "KernelBuffer.txt"
        found = False
        for logline in open (orgpath).readlines():
            if re.search ('Boot reason', logline) is not None:
                print orgpath, logline,
                found = True
                break
        if found is False:
            print orgpath, "<no boot reason>"


        klogfile = match.group ('path') + "/" + newboot + "/" + 'KernelBuffer.txt'

        found = False
        for logline in open (klogfile).readlines():
            if re.search ('Wrong Pinmux', logline) is not None:
                print klogfile, logline,
                found = True
                break
        if found is False:
            print klogfile, "<no pinmux line>"