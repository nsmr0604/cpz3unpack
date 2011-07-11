#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array
from decrypt import decrypt, encrypt, decryptPs2, encryptPs2
from lzss import decode, encode
import codecs
from scriptgetter import ScriptGetter

cpzFilename = ur"D:\eroge\明日の君と逢うために\data\pack\scriptback.cpz"
newFilename = ur"D:\eroge\明日の君と逢うために\data\pack\script.cpz"

relation_filename = ur"D:\data\workspace\asutame_text\etc\relation_release_0_5.txt"
source_path = ur"D:\data\workspace\asutame_text\source" + u"\\"
translated_path = ur"D:\data\workspace\asutame_text\已译" + u"\\"
source_encoding = "shift-jis"
translated_encoding = "gbk"

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
    fullHeader.fromfile(cpz, indexLength + 0x14)
    
    fullHeader[4:8] = array('B' , pack('L', indexCount))
    fullHeader[0x8:0xC] = array('B' , pack('L', indexLength))
    fullHeader[0x10:0x14] = array('B' , pack('L', keyMask))

keyMask = keyMask ^ 0x7BF4A539
#解密index
delta = 12 - 20

decrypt(fullHeader, 0x14, indexLength + 0x14, delta, keyMask)

#循环提取文件
newCpzHeader = array('B', fullHeader.tostring())
newCpzContent = array('B')
i = 0
pos = 0x14
while i < indexCount:
    itemIndexLength = unpack('L', fullHeader[pos:pos + 4])[0]
    itemLength = unpack('L', fullHeader[pos + 4:pos + 8])[0]
    itemOffset = unpack('L', fullHeader[pos + 8:pos + 0x0C])[0]
    itemFilename = fullHeader[pos + 0x18:pos + itemIndexLength].tostring().strip('\0')
    
        
    itemKeyMask = unpack('L', fullHeader[pos + 0x14:pos + 0x18])[0]
    itemKeyMask = itemKeyMask ^ 0xC7F5DA63
    with open(cpzFilename, 'rb') as cpz:
        cpz.seek(itemOffset + indexLength + 0x14, 0)
        item = array('B')
        item.fromfile(cpz, itemLength)
        
        getter = ScriptGetter(itemFilename + '.txt', relation_filename, source_path, translated_path, source_encoding, translated_encoding)
            
        #只封包relation中定义的文本
        if hasattr(getter, 'start_id'):
            skipcount = getter.start_id
            decrypt(item, 0, itemLength, 12, itemKeyMask)
            
            #解密&解压ps2
            
            decryptPs2(item, 0x30, itemLength - 0x30, unpack('L', item[0x0c:0x10])[0])
            itemHeader = item[0:0x30]
            itemContent = decode(item, 0x30, itemLength - 0x30)
            
            scriptLength = unpack('L', itemHeader[0x1C:0x20])[0]
            scriptOffset = len(itemContent) - scriptLength
            
            #读取txt文件，封入封包
            txtOffset = 0
            
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
#                                temp = codecs.decode(t[eq + 1:].strip('\r\n'), 'shift-jis')
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
                        if lastOffset[0] + lastOffset[1] - 1 + skipoffset>0:
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
            
            #加密
            encrypt(item, 0, len(itemContent) + 0x30, 12, itemKeyMask)
        
        itemOffset = len(newCpzContent)
        newCpzHeader[pos + 8:pos + 0x0C] = array('B', pack('L', itemOffset))
        
        itemLength = len(item)
        newCpzHeader[pos + 4:pos + 8] = array('B', pack('L', itemLength))
        
        #将此内容加入
        newCpzContent.fromstring(item.tostring())
        
        print itemFilename
        
    pos += itemIndexLength
    i += 1


delta = 12 - 20

encrypt(newCpzHeader, 0x14, indexLength + 0x14, delta, keyMask)

indexCount = unpack('L', newCpzHeader[4:8])[0] ^ 0x5E9C4F37
newCpzHeader[4:8] = array('B' , pack('L', indexCount))

indexLength = unpack('L', newCpzHeader[0x8:0xC])[0] ^ 0xF32AED17
newCpzHeader[0x8:0xC] = array('B' , pack('L', indexLength))
                        
keyMask = unpack('L', newCpzHeader[0x10:0x14])[0] ^ 0xDDDDDDDD
newCpzHeader[0x10:0x14] = array('B' , pack('L', keyMask))

with open(newFilename, 'wb') as newCpz:
    newCpzHeader.tofile(newCpz)
#    for i in (0x33 ,0x25 ,0xAD ,0xBA ,0xA5 ,0x22 ,0x31 ,0xF1 ,0x08 ,0x69 ,0x82 ,0xC2 ,0xFE ,0xCC ,0x16 ,0x47):
#        newCpz.write(chr(i))
    newCpzContent.tofile(newCpz) 
