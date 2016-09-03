#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import simplejson as json
import sys, os

from optparse import OptionParser


fscache = {}
def get_file(version, eventid):
    if eventid == 23:
        filename = "eventid%s_%s.txt" % (eventid, version)
        if fscache.has_key(filename) == False:
            fscache[filename] = open(filename, "wt")
        return fscache[filename]
    else:
        return None


def process_dir(dirname):
    for d in os.listdir (dirname):
        node_path = os.path.join (dirname, d)
        if os.path.isfile(node_path):
            print "processing file: %s" % (node_path)
            process_file (node_path)
        elif os.path.isdir(node_path):
            print "processing dir : %s" % (node_path)
            process_dir (node_path)


def process_file(filename):
    with open(filename) as fh:
        for line in fh:
            jobject = json.loads(line)
            if jobject.has_key ('ufversion'):
                ufver = jobject['ufversion']
            if jobject.has_key('events'):
                for event in jobject['events']:
                    if event.has_key('eventid'):
                        culfh = get_file(ufver, event['eventid'])
                        if culfh is not None:
                            culfh.write (json.dumps(event) + "\n")

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="logfile", help="cul log file to be inspected")
    parser.add_option("-d", "--dir", dest="dirname", help="directory containing CUL logs")

    (options, args) = parser.parse_args ()

    if options.logfile is not None:
        process_file(options.logfile)
    elif options.dirname is not None:
        process_dir (options.dirname)


#    print_event_detail(event_id_map)

if __name__ == '__main__':
    main()

