#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, traceback
import simplejson
import openpyxl
from optparse import OptionParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0



fscache = {}
def get_file(deviceid, version, country):
    filename = "%s_%s_%s.txt" % (deviceid, version, country)
    if fscache.has_key(filename) == False:
        fscache[filename] = open(filename, "wt")
    return fscache[filename]


all_events = None
lines = open ("part-00000.txt").readlines ()
for line in lines:
    line = line.strip()
    if len(line) is not 0:
        json = simplejson.loads(line)
        all_events = json["events"]

        if all_events is not None:
            fh = get_file(json["deviceid"], json["ufversion"], json["country"])
            for event in all_events:
                if event["eventid"] == 2:
                    fh.write("scrambled: %s " % (event["scrambled"]) + simplejson.dumps(event) + "\n")
                elif event["eventid"] != 23:
                    fh.write(simplejson.dumps(event) + "\n")
                else:
                    fh.write ("{'eventid':23, crashes: [\n")
                    for reboot in event["reboots"]:
                        fh.write (simplejson.dumps (reboot) + "\n")
                    fh.write ("], swfatal: [")
                    for fatal in event["swfatal"]:
                        fh.write(simplejson.dumps(fatal) + "\n")
                    fh.write ("], hwfatal: [")
                    for fatal in event["hwfatal"]:
                        fh.write(simplejson.dumps(fatal) + "\n")
                    fh.write ("]} \n")
