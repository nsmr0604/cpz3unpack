#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array
from decrypt import decrypt, encrypt, decryptPs2, encryptPs2
from lzss import decode, encode

cpzFilename = ur"C:\games\明日の君と逢うために\data\pack\script.cpz"
newFilename = ur"C:\games\明日の君と逢うために\data\pack\script2.cpz"
outputFolder = ur"C:\games\明日の君と逢うために\data\pack\script\\"

with open(ur"C:\games\明日の君と逢うために\data\pack\script\snky00.ps2.txt", 'rb') as text:
    for t in text:
        if t.startswith(';'):
            continue
        eq = t.find('=')
        print t[eq + 1:].strip('\r\n')
