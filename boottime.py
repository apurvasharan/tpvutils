#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os, sys, re, traceback
from monotonic import get_lines_with_monotonic

from optparse import OptionParser

PATTERNS = ["TVPower System", ]

def process (filename, cpatterns):
    for line in get_lines_with_monotonic(filename):
        for p in cpatterns:
            if p.search(line) is not None:
                print line


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="logfile", help="merged log file to be processed")

    (options, args) = parser.parse_args ()

    if options.logfile is not None:
        cpatterns = []
        for p in PATTERNS:
            cpatterns.append (re.compile(p, re.IGNORECASE))
        process(options.logfile, cpatterns)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
