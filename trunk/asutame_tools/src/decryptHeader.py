#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array

originalKey = array('B')
originalKeyTuple = (0x5E , 0x4A , 0x0D , 0x4D , 0xE1 , 0xF3 , 0xAB , 0xB3 ,
                0x6D , 0x33 , 0x37 , 0x3C , 0xF3 , 0xF5 , 0xC3 , 0x86,
                 0x89 , 0x9B , 0x4F , 0x7D , 0x11 , 0xDE , 0xD7 , 0x58 ,
                 0x8D , 0x77 , 0x67 , 0x63 , 0x29 , 0x46 , 0xF3 , 0xA5 ,
                 0xB5 , 0xA4 , 0x7F , 0x06 , 0x42 , 0xE7 , 0x0A , 0xED ,
                 0xCC , 0x50 , 0x94 , 0xB1 , 0x5A , 0x4A , 0x20 , 0xE7 ,
                 0xF5 , 0x04 , 0xAF , 0xD9 , 0x7F , 0x68 , 0x3B , 0x5D ,
                 0xFD , 0xA6 , 0xC7 , 0xC1 , 0x89 , 0x22 , 0x50 , 0xFC)
for byte in originalKeyTuple:
    originalKey.append(byte)
del originalKeyTuple

def decrypt(buf, offset, length, delta, rolcl, keyMask):
    key = array('B')
    for i in xrange(0, 16):
        tmp = unpack('L', originalKey[i * 4:i * 4 + 4])[0]
        tmp = (tmp + keyMask) & 0xFFFFFFFF
        key.fromstring(array('B', pack('L', tmp)).tostring())
    
    eax = keyMask
    eax = eax >> 4
    eax = eax ^ keyMask
    eax = eax >> 4
    eax = eax ^ keyMask
    eax = eax >> 4
    eax = eax ^ keyMask
    eax = eax >> 4
    eax = eax ^ keyMask
    eax = eax >> 4
    eax = eax ^ keyMask
    eax = eax >> 4
    eax = eax ^ keyMask
    eax = eax >> 4
    eax = eax ^ keyMask
    eax = eax ^ 0xFFFFFFFD
    eax = eax & 0x0F
    rolcl = eax + 8
    
    i = offset
    
    while(1):
        keyIndex = (i + delta) & 0x3F
        ebp = unpack('L', buf[i:i + 4])[0] ^ unpack('L', key[keyIndex:keyIndex + 4])[0]
        ebp += 0x6E58A5C2
        ebp = ebp & 0xFFFFFFFF
        
        ebp = rol(ebp, rolcl)
        buf[i:i + 4] = array('B', pack('L', ebp))
        i = i + 4
        if i >= length:
            break


def rol(num, count):
        num1 = (num << count) & 0xFFFFFFFF
        num2 = (num >> (0x20 - count)) & 0xFFFFFFFF
        return num1 | num2
