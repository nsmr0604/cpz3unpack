#!/usr/bin/env python
# -*- coding: utf-8 -*-
from array import array

N = 2048
F = 23
THRESHOLD = 1

def decode(inputBuf, offset, length):
    i = 0
    j = 0
    k = 0
    c = 0
    p = offset
    flags = 0
    
    text_buf = array('B', '\0' * (N + F - 1))
    outputBuf = array('B')
    r = N - F
    
    while(1):
        flags = flags >> 1
        if flags & 256 == 0:
            if p >= length:
                break
            c = inputBuf[p]
            p += 1
            flags = c | 0xff00
        if flags & 1:
            if p >= length:
                break
            c = inputBuf[p]
            p += 1
            outputBuf.append(c)
            text_buf[r] = c
            r = r + 1
            r &= N - 1
        else:
            if p >= length:
                break
            i = inputBuf[p]
            p += 1
            if p >= length:
                break
            j = inputBuf[p]
            p += 1
            i |= ((j & 0xe0) << 4)
            j = (j & 0x1f) + THRESHOLD
            for k in xrange(0, j + 1):
                c = text_buf[(i + k) & (N - 1)]
                outputBuf.append(c)
                text_buf[r] = c
                r += 1
                r &= N - 1
    return outputBuf







