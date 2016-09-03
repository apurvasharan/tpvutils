#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os, sys, re, traceback
from optparse import OptionParser
from datetime import datetime, timedelta

LOG_PATTERN = r'(?P<dt>\d\d-\d\d) (?P<tm>\d\d:\d\d:\d\d\.\d\d\d) (?P<pid>[ \d]{5}) (?P<tid>[ \d]{5}) (?P<log>.*)'
SKIP_PATTERNS = ['beginning of main', 'beginning of system', 'beginning of crash', 'Boot_\d\d\d\d.*']

# Assumption: This should be invoked with merged logcat files corresponding to cold boot cycles
# Execute: <execname> <merged logcat for the boot cycle>

running_dttm = None
prev_dttm = None
running_seconds = 0.0

JUMP = 300 # 5mins


def get_mapped_dttm (new_dt, new_tm):
    global prev_dttm, running_dttm, running_seconds

    new_dttm = datetime.strptime (new_dt + " " + new_tm, "%m-%d %H:%M:%S.%f")

    if prev_dttm == None:
        prev_dttm = new_dttm

    if running_dttm == None:
        running_dttm = new_dttm

    td = new_dttm - prev_dttm

    timejump = ((td > timedelta(seconds=JUMP)) or (td < timedelta(seconds=0)))

    if timejump is False:
        running_dttm = running_dttm + td
        running_seconds += td.days * 24*3600 + td.seconds + td.microseconds/1000000.0

    prev_dttm = new_dttm

    return (running_dttm, running_seconds)


def prefix_monotonic(line):
    matches = re.match(LOG_PATTERN, line)

    if matches is not None:
        dt = matches.group('dt')
        tm = matches.group('tm')

        (mapped_dttm, running_seconds) = get_mapped_dttm (dt, tm)
        return "%4.3f :: %s" % (running_seconds, line)
    else:
        print "!!! Unidentified log template !!! [%s]" % line


def get_lines_with_monotonic(filename):
    with open (filename, "rb") as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0:
                skip = False
                for p in SKIP_PATTERNS:
                    if re.search (p, line) is not None:
                        skip = True
                if skip is False:
                    yield prefix_monotonic(line)
