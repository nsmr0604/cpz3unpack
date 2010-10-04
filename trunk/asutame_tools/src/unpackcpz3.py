#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array
from decrypt import decrypt, decryptPs2, decryptPb3
from lzss import decode

cpzFilename = ur"Z:\games\明日の君と逢うために\data\pack\script.cpz"
newFilename = ur"Z:\games\明日の君と逢うために\data\pack\script.header"
outputFolder = ur"Z:\games\明日の君と逢うために\data\pack\script\\"

#解密文件头
with open(cpzFilename, 'rb') as cpz:
    header = array('B')
    header.fromfile(cpz, 0x18)
    
    indexCount = unpack('L', header[4:8])[0] ^ 0x5E9C4F37
    header[4:8] = array('B' , pack('L', indexCount))
    
    indexLength = unpack('L', header[0x8:0xC])[0] ^ 0xF32AED17
    header[0x8:0xC] = array('B' , pack('L', indexLength))
                            
    keyMask = unpack('L', header[0x10:0x14])[0] ^ 0xDDDDDDDD
    header[0x10:0x14] = array('B' , pack('L', keyMask))
    
with open(cpzFilename, 'rb') as cpz:
    fullHeader = array('B')
    fullHeader.fromfile(cpz, indexLength + 4)
    
    fullHeader[4:8] = array('B' , pack('L', indexCount))
    fullHeader[0x8:0xC] = array('B' , pack('L', indexLength))
    fullHeader[0x10:0x14] = array('B' , pack('L', keyMask))

keyMask = keyMask ^ 0x7BF4A539
#解密index
delta = 12 - 20

decrypt(fullHeader, 0x14, indexLength + 4, delta, keyMask)

#循环提取文件

i = 0
pos = 0x14
while i < indexCount:
    itemIndexLength = unpack('L', fullHeader[pos:pos + 4])[0]
    itemLength = unpack('L', fullHeader[pos + 4:pos + 8])[0]
    itemOffset = unpack('L', fullHeader[pos + 8:pos + 0x0C])[0]
    itemFilename = fullHeader[pos + 0x18:pos + itemIndexLength].tostring().strip('\0')
#    if itemFilename != 'config02_chip.pb3':
#        i += 1
#        pos += itemIndexLength
#        continue
    itemKeyMask = unpack('L', fullHeader[pos + 0x14:pos + 0x18])[0]
    itemKeyMask = itemKeyMask ^ 0xC7F5DA63
    with open(cpzFilename, 'rb') as cpz:
        cpz.seek(itemOffset + indexLength + 0x14, 0)
        item = array('B')
        item.fromfile(cpz, itemLength)
        #item = cpz.read(itemLength)
        decrypt(item, 0, itemLength, 12, itemKeyMask)
        
        
        with open(outputFolder + itemFilename, 'wb') as outputFile:
        
            #解密&解压ps2
            if itemFilename.endswith('.ps2'):
                decryptPs2(item, 0x30, itemLength - 0x30, unpack('L', item[0x0c:0x10])[0])
                itemHeader = item[0:0x30]
                itemContent = decode(item, 0x30, itemLength - 0x30)
                
                scriptLength = unpack('L', itemHeader[0x1C:0x20])[0]
                scriptOffset = len(itemContent) - scriptLength

                with open(outputFolder + itemFilename + '.txt', 'wb') as outputTxtFile:
                    count = 0
                    for j in xrange(0, scriptOffset - 8):
                        if unpack('L', itemContent[j:j + 4])[0] == 0x01200201:
                            sentenceOffset = unpack('L', itemContent[j + 4:j + 8])[0]
                            sentence = itemContent[scriptOffset + sentenceOffset:scriptOffset + sentenceOffset + 255].tostring()
                            sentence = sentence.split('\0')[0]
                            if sentence == '':
                                continue
                            count += 1
                            outputTxtFile.write(';' + sentence)
                            outputTxtFile.write('\r\n')
                            outputTxtFile.write(str(count) + '=' + sentence)
                            outputTxtFile.write('\r\n')
                
                #outputFile.write(item)
                itemHeader.tofile(outputFile)
                itemContent.tofile(outputFile)
                #item.tofile(outputFile)
            elif itemFilename.endswith('.pb3'):
                decryptPb3(item, 0, itemLength)
                item.tofile(outputFile)
            else:
                item.tofile(outputFile)
            
    pos += itemIndexLength
    i += 1

#写入
#with open(newFilename, 'wb') as newCpz:
#    fullHeader.write(newCpz)
