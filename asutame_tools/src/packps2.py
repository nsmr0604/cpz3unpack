#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array
from decrypt import decrypt, encrypt, decryptPs2, encryptPs2
from lzss import decode, encode
import os
from scriptgetter import ScriptGetter
import codecs

ps2Filename = ur"Z:\games\明日の君と逢うために\data\pack\startback.ps2"
newTxtFilename = ur"Z:\games\明日の君と逢うために\data\pack\start.ps2.txt"
newFilename = ur"Z:\games\明日の君と逢うために\data\pack\start.ps2"
outputFolder = ur"Z:\games\明日の君と逢うために\data\pack\\"

relation_filename = ur"C:\workspace\asutame_text\etc\\relation_release_0_0.txt"
source_path = ur"C:\workspace\asutame_text\source" + u"\\"
translated_path = ur"C:\workspace\asutame_text\已译" + u"\\"
source_encoding = "shift-jis"
translated_encoding = "gbk"

itemFilename='start.ps2'

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

    getter = ScriptGetter(itemFilename + '.txt', relation_filename, source_path, translated_path, source_encoding, translated_encoding)
        
    #只封包relation中定义的文本
    if hasattr(getter, 'start_id'):
        skipcount = getter.start_id
        
        #解密&解压ps2
        
#        decryptPs2(item, 0x30, itemLength - 0x30, unpack('L', item[0x0c:0x10])[0])
#        itemHeader = item[0:0x30]
#        itemContent = decode(item, 0x30, itemLength - 0x30)
#        
#        scriptLength = unpack('L', itemHeader[0x1C:0x20])[0]
#        scriptOffset = len(itemContent) - scriptLength
        
        #读取txt文件，封入封包
        txtOffset = 1
        
        #新文本的偏移和长度
        textOffset = {}
        text = ''
        count = 1
        #<则不动的文本的序号297
#            skipcount = 297
        #不跳过的第一条文本的原偏移。从这个位置开始放入新文本
        skipoffset = 0
            
        with open(source_path + itemFilename + '.txt', 'rb') as inputTxtFile:
            for t in inputTxtFile:
                if t.startswith(';'):
                    continue
                if len(t.strip()) == 0:
                    continue
                if count < skipcount and t.find('=') >= 0:
                    count += 1
                    continue
                eq = t.find('=')
                line = t[eq + 1:].strip('\r\n') + '\0'
                newline = getter.get_script(codecs.decode(t.split('=')[0], source_encoding))
                if newline:
                    try:
                        temp = codecs.decode(t[eq + 1:].strip('\r\n'), 'shift-jis')
                        line = codecs.encode(newline, translated_encoding) + '\0'
                        pass
                    except UnicodeEncodeError:
                        print "ERROR: can't encode " + newline
                
                textOffset[count] = (len(text), len(line))
                text += line
                count += 1
        count = 1
        lastOffset = (0, 0)
        for j in xrange(0, scriptOffset - 8):
            if unpack('L', itemContent[j:j + 4])[0] == 0x01200201:
                sentenceOffset = unpack('L', itemContent[j + 4:j + 8])[0]
                sentence = itemContent[scriptOffset + sentenceOffset:scriptOffset + sentenceOffset + 255].tostring()
                sentence = sentence.split('\0')[0]
                if sentence == '':
                    itemContent[j + 4:j + 8] = array('B', pack('L', lastOffset[0] + lastOffset[1] - 1 + skipoffset))
                    #itemContent[j + 4:j + 8] = array('B', pack('L', 0))
                    continue
                if count < skipcount:
                    count += 1
                    continue
                if count == skipcount:
                    skipoffset = sentenceOffset
                
                itemContent[j + 4:j + 8] = array('B', pack('L', textOffset[count][0] + skipoffset))
                lastOffset = textOffset[count]
                count += 1
        
        textArray = array('B', text)
        itemHeader[0x1C:0x20] = array('B', pack('L', len(textArray)))
        #itemHeader[0x28:0x2C] = array('B', pack('L', scriptOffset + skipoffset + len(textArray)))
        itemHeader[0x28:0x2C] = array('B', pack('L', scriptOffset * 2 + skipoffset + len(textArray)))

        #itemContent = itemContent[0:scriptOffset] + textArray
        itemContent = itemContent[0:scriptOffset + skipoffset] + textArray

        #压缩
        itemContent = encode(itemContent, 0, len(itemContent))
        item = itemHeader + itemContent
        encryptPs2(item, 0x30, len(itemContent), unpack('L', item[0x0c:0x10])[0])
        
    with open(newFilename, 'wb') as newFile:
        item.tofile(newFile)
 
    

#写入
#with open(newFilename, 'wb') as newCpz:
#    fullHeader.write(newCpz)
