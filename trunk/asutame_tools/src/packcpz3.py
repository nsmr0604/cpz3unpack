#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, pack
from array import array
from decrypt import decrypt, decryptPs2
from lzss import decode

cpzFilename = ur"C:\games\明日の君と逢うために\data\pack\script.cpz"
newFilename = ur"C:\games\明日の君と逢うために\data\pack\script.header"
outputFolder = ur"C:\games\明日の君と逢うために\data\pack\script\\"
