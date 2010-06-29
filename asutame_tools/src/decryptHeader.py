#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array

def decrypt(buf, offset, length, delta, key):
    i = offset
    while(1):
        keyIndex = (i + delta) & 0x3F
        ebp = unpack('L', buf[i:i + 4])[0] ^ unpack('L', key[keyIndex:keyIndex + 4])[0]
        ebp += 0x6E58A5C2
        ebp = ebp & 0xFFFFFFFF
        
        #ROL EBP,13
        ebp1 = (ebp << 0x13) & 0xFFFFFFFF
        ebp2 = (ebp >> 0x0D) & 0xFFFFFFFF
        ebp = ebp1 | ebp2
        buf[i:i + 4] = array('B', pack('L', ebp))
        i = i + 4
        if i >= length:
            break
