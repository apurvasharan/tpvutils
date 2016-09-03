#!/bin/env python

import os, glob, re, sys


def merge_bootlog (boot_dir):
    cwd = os.getcwd()
    
    if os.path.exists (boot_dir) == False:
        return

    os.chdir (boot_dir)
    logfiles = []

    for file in glob.glob ("logcat.txt*"):
        logfiles.append (file)

    max = 0
    for name in logfiles:
        m = re.search (r'logcat\.txt\.?(?P<extn>.*)', name) 
        if m != None:
            x = m.group ("extn")
            x = x.strip ()
            if len (x) != 0:
                if int (x) > max:
                    max = int (x)
            else:
                max = 0

    sequence = ["logcat.txt.%d" % i for i in range (1, max+1)]

    for s in sequence:
        if os.path.exists (s):
            yield (s)

    if os.path.exists ("logcat.txt"):
        yield ("logcat.txt")

    os.chdir (cwd)


def merge_log ():
    bootdirs = []
    for dirname in glob.glob ("Boot*"):
        bootdirs.append (dirname)

    max = 0
    for name in bootdirs:
        m = re.search (r'Boot_(?P<extn>\d+)', name)
        if m != None:
            x = m.group ("extn")
            x = x.strip ()
            if len(x) != 0:
                if int (x) > max:
                    max = int (x)
            else:
                max = 0

    sequence = ["Boot_%04d" % i for i in range (0, max + 1)]

    m = open ("MergeLog.txt", "wb")
    for s in sequence:
        if os.path.exists (os.path.join (s, "version.txt")):
            content = open (os.path.join (s, "version.txt")).read()
            m.write ("\n%s: %s\n" % (s, content.strip()))
            
        for fname in merge_bootlog (s):
            m.write(open(fname, "rb").read())

    m.close()


if __name__ == '__main__':
    if len(sys.argv) == 1: # only the python script
        merge_log ()
    else:
        for x in sys.argv[1:]:
            m = open ("%s_MergeLog.txt" % x, "wb")

            if os.path.exists (os.path.join (x, "version.txt")):
                content = open (os.path.join (x, "version.txt")).read()
                m.write ("\n%s: %s\n" % (x, content.strip()))

            for fname in merge_bootlog (x):
                m.write(open(fname, "rb").read())

            m.close ()
