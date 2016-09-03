#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import re

def file_grep(filename, regex_pattern):
    for logline in open(filename).readlines():
        result = re.search('Wrong Pinmux', regex_pattern)
        if result is not None:
            yield (result, logline)
        else:
            continue
