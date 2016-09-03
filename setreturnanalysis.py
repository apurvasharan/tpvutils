#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, traceback
import openpyxl
from optparse import OptionParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

COLUMNS_NEEDED = ['platform', 'Symptom Code 1--Description', 'Regular SW number IN', 'Function', 'WO Date',
                  'Repair Completed Date', 'Product No', 'Model No', 'Request Type']
RAW_DATA_SHEET_NAME = 'Data From TCA'


def collect_data (excelfile):
    colids_needed = []
    exceldata = []

    wb = openpyxl.load_workbook(excelfile, read_only=True)
    ws = wb[RAW_DATA_SHEET_NAME]

    rcount = 0
    for row in ws.rows:
        rcount += 1
        if rcount == 1: # 1 indexed - a'la excel
            for header in COLUMNS_NEEDED:
                colid = 0
                for cell in row:
                    colid += 1   # 1 indexed - a'la excel
                    if cell.value.strip() == header:
                        colids_needed.append (colid)
                        break
        else:
            ldata = []
            colid = 0
            for cell in row:
                colid += 1
                ldata.append (cell.value)

            data = {}
            for colname, colid in zip(COLUMNS_NEEDED, colids_needed):
                data [colname] = ldata[colid-1]
            exceldata.append (data)
    return exceldata


# def data_without_function_column()

# Need :
# 1. SW category - root categories count of returns
# 2. Work Order Date - months count
# 3. Repair completion - months count

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="excel file name")
    parser.add_option("-m", "--multifile", dest="multifile", help="text file containing multiple excel files")

    (options,args) = parser.parse_args()
    if options.file is not None:
        all_data = collect_data(options.file)
    elif options.multifile is not None:
        all_data = []
        for line in open(options.multifile, "rt").readlines():
            if line is not None and len (line.strip()) != 0:
                print "Processing file: %s" % (line.strip())
                all_data.extend(collect_data(line.strip()))
    else:
        parser.print_help()

    # all data has all data sets
    print len (all_data)


if __name__ == '__main__':
    main()