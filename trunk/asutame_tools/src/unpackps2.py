#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array
from decrypt import decrypt, decryptPs2, decryptPb3
from lzss import decode
import os

ps2Filename = ur"Z:\games\明日の君と逢うために\data\pack\start.ps2"
newFilename = ur"Z:\games\明日の君と逢うために\data\pack\start.ps2.txt"
outputFolder = ur"Z:\games\明日の君と逢うために\data\pack\\"

#解密文件头
with open(ps2Filename, 'rb') as cpz:
    item = array('B')
    itemLength = os.stat(ps2Filename).st_size
    item.fromfile(cpz,itemLength)
    #item = cpz.read(itemLength)
#    decrypt(item, 0, itemLength, 12, itemKeyMask)
    
    #解密&解压ps2
    decryptPs2(item, 0x30, itemLength - 0x30, unpack('L', item[0x0c:0x10])[0])
    itemHeader = item[0:0x30]
    itemContent = decode(item, 0x30, itemLength - 0x30)
    
    scriptLength = unpack('L', itemHeader[0x1C:0x20])[0]
    scriptOffset = len(itemContent) - scriptLength

    with open(newFilename, 'wb') as outputTxtFile:
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
    

#写入
#with open(newFilename, 'wb') as newCpz:
#    fullHeader.write(newCpz)
