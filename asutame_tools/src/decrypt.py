#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array
try:
    import c_decrypt
except:
    c_decrypt = False
    
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

def decrypt(buf, offset, length, delta, keyMask):
    if c_decrypt:
        bufStr = buf[0:0+length+offset].tostring()
        buf[0:0+length+offset] = array('B', c_decrypt.decrypt(bufStr, offset, length, delta, keyMask))
#        buf[0:0+length+offset].tofile(open('d:/temp/c.lzss','wb'))
#        raise self
        return
    key = array('B')
    
    padding = length & 0x03

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
        ebp = unpack('L', buf[i:i + 4])[0]
        ebp = ebp ^ unpack('L', key[keyIndex:keyIndex + 4])[0]
        ebp += 0x6E58A5C2
        ebp = ebp & 0xFFFFFFFF
        
        ebp = rol32(ebp, rolcl)

        buf[i:i + 4] = array('B', pack('L', ebp))
        i = i + 4
        if i >= length - 3:
            break
    
    #处理尾部
    j = i
    while padding > 0:
        keyIndex = (j + delta) & 0x3F
        eax = unpack('L', key[keyIndex:keyIndex + 4])[0]
        ecx = padding * 4
        eax = eax >> (ecx & 0x0f)
        j = j + 4
        i = i + 1
        al = eax & 0x0ff
        al = al ^ buf[i - 1]
        al = al + 0x52
        al = al & 0x0ff
        padding = padding - 1
        buf[i - 1] = al

def encrypt(buf, offset, length, delta, keyMask):
    if c_decrypt:
        bufStr = buf[0:0+length+offset].tostring()
        buf[0:0+length+offset] = array('B', c_decrypt.encrypt(bufStr, offset, length, delta, keyMask))
#        buf[0:0+length+offset].tofile(open('d:/temp/c.lzss','wb'))
#        raise self
        return
    key = array('B')
    
    padding = length & 0x03

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
        
        ebp = unpack('L', buf[i:i + 4])[0]
        ebp = ror32(ebp, rolcl)
        ebp = ebp & 0xFFFFFFFF
        ebp -= 0x6E58A5C2
        ebp = ebp & 0xFFFFFFFF
        ebp = ebp ^ unpack('L', key[keyIndex:keyIndex + 4])[0]
        
        buf[i:i + 4] = array('B', pack('L', ebp))
        
        i = i + 4
        if i >= length - 3:
            break
    
    #处理尾部
    j = i
    while padding > 0:
        keyIndex = (j + delta) & 0x3F
        
        eax = unpack('L', key[keyIndex:keyIndex + 4])[0]
        ecx = padding * 4
        eax = eax >> (ecx & 0x0f)
        j = j + 4
        i = i + 1
        al = eax & 0x0ff
        
        dl = buf[i - 1]
        dl = dl - 0x52
        dl = dl & 0xff
        buf[i - 1] = al ^ dl
        
#        print al ^ dl
        
        padding = padding - 1
    
#    buf[0:0+length+offset].tofile(open('d:/temp/a.lzss','wb'))
#    raise self
    
def rol32(num, count):
    num1 = (num << count) & 0xFFFFFFFF
    num2 = (num >> (0x20 - count)) & 0xFFFFFFFF
    return num1 | num2

def ror32(num, count):
    num1 = (num >> count) & 0xFFFFFFFF
    num2 = (num << (0x20 - count)) & 0xFFFFFFFF
    return num1 | num2

def ror8(num, count):
    num1 = (num >> count) & 0xFF
    num2 = (num << (0x08 - count)) & 0xFF
    return num1 | num2

def rol8(num, count):
    num1 = (num << count) & 0xFF
    num2 = (num >> (0x08 - count)) & 0xFF
    return num1 | num2


def decryptPs2(buf, offset, length, key):
    if c_decrypt:
        bufStr = buf[offset:offset+length].tostring()
#        print len(array('B', c_decrypt.encryptPs2(bufStr, key)))
        buf[offset:offset+length] = array('B', c_decrypt.decryptPs2(bufStr, key))
#        print  array('B', c_decrypt.encryptPs2(bufStr, key))[0]
        return
    ecx = key
    eax = ecx
    eax >>= 0x14
    edx = eax % 5
    eax = eax / 5
    eax = ecx
    eax >>= 0x18
    ecx >>= 3
    al = eax & 0xff
    cl = ecx & 0xff
    al += cl
    al &= 0xff
    dl = edx & 0xff
    dl += 1
    ecx = dl
    cl = ecx & 0xff
    
    for i in xrange(offset, offset + length):
        dl = buf[i]
        dl = dl - 0x7C
        dl = dl & 0xFF
        dl = dl ^ al
        dl = ror8(dl, cl)
        buf[i] = dl
    
    
    
def encryptPs2(buf, offset, length, key):
#    print length
    if c_decrypt:
        bufStr = buf[offset:offset+length].tostring()
#        print len(array('B', c_decrypt.encryptPs2(bufStr, key)))
        buf[offset:offset+length] = array('B', c_decrypt.encryptPs2(bufStr, key))
#        print  array('B', c_decrypt.encryptPs2(bufStr, key))[0]
        return
    ecx = key
    eax = ecx
    eax >>= 0x14
    edx = eax % 5
    eax = eax / 5
    eax = ecx
    eax >>= 0x18
    ecx >>= 3
    al = eax & 0xff
    cl = ecx & 0xff
    al += cl
    al &= 0xff
    dl = edx & 0xff
    dl += 1
    ecx = dl
    cl = ecx & 0xff
    
    for i in xrange(offset, offset + length):
        dl = buf[i]
        dl = rol8(dl, cl)
        dl = dl ^ al
        dl = dl & 0xFF
        dl = dl + 0x7c
        dl = dl & 0xFF
        buf[i] = dl
    
    
    
#offset是指文件头（'PB3'所在的位置）
def decryptPb3(buf, offset, length):
    key = unpack('H', buf[length - 3:length - 1])[0]
    for i in xrange(0x08, 0x34, 2):
        buf[i] ^= (key & 0xff)
        buf[i + 1] ^= (key & 0xff00) >> 8

    esi = length - 0x2f
    for i in xrange(0, 0x2c):
        buf[0x08 + i] = (buf[0x08 + i] - buf[esi + i]) & 0xff
    
    
    
    
    
    
