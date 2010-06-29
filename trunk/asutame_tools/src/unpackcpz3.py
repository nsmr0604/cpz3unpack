#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array
from decryptHeader import decrypt

cpzFilename = ur"C:\games\明日の君と逢うために\data\pack\script.cpz"
newFilename = ur"C:\games\明日の君と逢うために\data\pack\script.header"
outputFolder = ur"C:\games\明日の君と逢うために\data\pack\script\\"

#密钥
key = array('B')
keyTuple = (0x9F, 0x78, 0x83, 0xC6, 0x22, 0x22, 0x22, 0x2D,
        0xAE, 0x61, 0xAD, 0xB5, 0x34, 0x24, 0x3A, 0x00,
        0xCA, 0xC9, 0xC5, 0xF6, 0x52, 0x0C, 0x4E, 0xD2,
        0xCE, 0xA5, 0xDD, 0xDC, 0x6A, 0x74, 0x69, 0x1F,
        0xF6, 0xD2, 0xF5, 0x7F, 0x83, 0x15, 0x81, 0x66,
        0x0D, 0x7F, 0x0A, 0x2B, 0x9B, 0x78, 0x96, 0x60,
        0x36, 0x33, 0x25, 0x53, 0xC0, 0x96, 0xB1, 0xD6,
        0x3E, 0xD5, 0x3D, 0x3B, 0xCA, 0x50, 0xC6, 0x75)
for byte in keyTuple:
    key.append(byte)

del keyTuple

#解密文件头
with open(cpzFilename, 'rb') as cpz:
    header = array('B')
    header.fromfile(cpz, 0x18)
    
    indexCount = unpack('L', header[4:8])[0] ^ 0x5E9C4F37
    header[4:8] = array('B' , pack('L', indexCount))
    
    indexLength = unpack('L', header[0x8:0xC])[0] ^ 0xF32AED17
    header[0x8:0xC] = array('B' , pack('L', indexLength))
                            
    unknownUse = unpack('L', header[0x10:0x14])[0] ^ 0xDDDDDDDD
    header[0x10:0x14] = array('B' , pack('L', unknownUse))
    
with open(cpzFilename, 'rb') as cpz:
    fullHeader = array('B')
    fullHeader.fromfile(cpz, indexLength + 4)
    
    fullHeader[4:8] = array('B' , pack('L', indexCount))
    fullHeader[0x8:0xC] = array('B' , pack('L', indexLength))
    fullHeader[0x10:0x14] = array('B' , pack('L', unknownUse))

#解密index
delta = 12 - 20

decrypt(fullHeader, 0x14, indexLength + 4, delta, key)

#循环提取文件

i = 0
pos = 0x14
while i < indexCount:
    itemIndexLength = unpack('L', fullHeader[pos:pos + 4])[0]
    itemLength = unpack('L', fullHeader[pos + 4:pos + 8])[0]
    itemOffset = unpack('L', fullHeader[pos + 8:pos + 0x0C])[0]
    itemFilename = fullHeader[pos + 0x18:pos + itemIndexLength].tostring().strip('\0')
    with open(cpzFilename, 'rb') as cpz:
        cpz.seek(itemOffset + indexLength, 0)
        item = array('B')
        item.fromfile(cpz, itemLength)
        #item = cpz.read(itemLength)
        decrypt(item, 0, itemLength - 4, -8, key)
        with open(outputFolder + itemFilename, 'wb') as outputFile:
            #outputFile.write(item)
            item.tofile(outputFile)
    pos += itemIndexLength
    i += 1

#写入
with open(newFilename, 'wb') as newCpz:
    fullHeader.write(newCpz)
