#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os, sys, re, traceback
from monotonic import get_lines_with_monotonic

from optparse import OptionParser


def process (filename, cpattern):
    for line in get_lines_with_monotonic(filename):
        if cpattern.search(line) is not None:
            print line


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="logfile", help="merged log file to be processed")
    parser.add_option("-l", "--log", dest="log", help="Log line (in double quoted string)")

    (options, args) = parser.parse_args ()

    if options.logfile is not None and options.log is not None:
        cpattern = re.compile (options.log, re.IGNORECASE)
        process(options.logfile, cpattern)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
