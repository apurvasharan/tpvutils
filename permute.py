#!/usr/bin/env python
# -*- coding: utf-8 -*-

str = "abcdefg"

def insert(ch, target):
    ret = []
    mlen = len(target)
    for i in range(mlen+1):
        ret.append(target[:i] + ch + target[i:])
    return ret

def permute(str):
    result = []
    for ch in str:
        if len (result) == 0:
            lresult = [ch]
        else:
            lresult = []
            for res in result:
                lresult.extend(insert(ch, res))
        result = lresult
    return result

print len(permute("abcdefgij"))