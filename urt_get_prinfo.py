#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, traceback
from optparse import OptionParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from django.utils.encoding import smart_str

VERBOSE = True

FIELDS = ['Issue Code', 'Pillar', 'Subsystem', 'APK', 'Regression', 'State', 'Assignee', 'Deadline', 'Severity', 'Reproduction rate', 'Create', 'Subject']

def login (driver, wait):
    driver.get ("http://fwtrack.tpvaoc.com/")
    element = wait.until(EC.presence_of_element_located((By.ID, "txtEmail")))
    driver.find_element_by_id ('txtEmail').send_keys ('apurva.sharan@tpvision.com')
    driver.find_element_by_id ('txtPassword').send_keys ('rafi4$pur')
    driver.find_element_by_id ('btnLogin').click ()
    wait.until (EC.presence_of_element_located ((By.ID, 'ctl00_Siteheader1_txtProblemID')))


def get_pr_info (driver, wait, prnum):
    info = {}
    driver.find_element_by_id ("ctl00_Siteheader1_txtProblemID").send_keys (prnum)
    driver.find_element_by_id ('ctl00_Siteheader1_btnGoToProblem').click ()
    wait.until (EC.presence_of_element_located ((By.ID, 'ctl00_CP1_tblProblemInfo')))

    table_rows = driver.find_elements_by_xpath ('//*[@id="ctl00_CP1_tblProblemInfo"]/tbody/tr')
    for row in table_rows:
        try:
            info [row.find_element_by_class_name ('ProblemInfoItemName').text] = row.find_element_by_class_name ('ProblemInfoItemValue').text
        except:
            pass

    table_rows = driver.find_elements_by_xpath ('//*[@id="ctl00_CP1_tblProblemAttributes"]/tbody/tr')
    for row in table_rows:
        try:
            info [row.find_element_by_class_name ('ProblemInfoItemName').text] = row.find_element_by_class_name ('ProblemInfoItemValue').text
        except:
            pass

    return info

def get1pr (prnum):
    driver = webdriver.PhantomJS()
    wait = WebDriverWait(driver, 10)
    login (driver, wait)
    info = get_pr_info (driver, wait, prnum)
    driver.quit ()
    return [info]

def getNprs (prfile):
    prs = open (prfile, "rt").readlines()

    driver = webdriver.PhantomJS()
    wait = WebDriverWait(driver, 10)
    login (driver, wait)

    info = []
    for line in prs:
        prnum = line.strip()
        if len(prnum) != 0:
            if VERBOSE: print "Processing: [%s]" % prnum
            info.append (get_pr_info (driver, wait, prnum))

    driver.quit()
    return info

def keep_required (data):
    ret = []
    for d in data:
        kv = {}
        for k in d.keys ():
            if k in FIELDS:
               kv [k] = d[k]
        ret.append (kv)
    return ret

def print_formatted_data (data):
    print "$$$$". join ("%s" % s for s in FIELDS)
    for d in data:
        values = []
        for f in FIELDS:
            if f in d.keys ():
                if f == 'Create':
                    values.append (d[f].split ()[-2])
                else:
                    values.append (d[f])
            else:
                values.append ("-")
        print "$$$$".join (smart_str (u"%s" % x) for x in values)

def main ():
    parser = OptionParser()
    parser.add_option("-s", "--single", dest="prnum", help="Single PR number")
    parser.add_option("-m", "--multi", dest="prfile", help="Text file containing PR numbers, one in one line")

    (options, args) = parser.parse_args()

    if options.prnum is not None:
        data = get1pr (options.prnum)
    elif options.prfile is not None:
        data = getNprs (options.prfile)
    else:
        parser.print_help()
        exit(0)

    data = keep_required (data)

    print_formatted_data (data)

if __name__ == '__main__':
    main ()
