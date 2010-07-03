#!/usr/bin/env python
# -*- coding: utf-8 -*-

inputFilename='/Users/Shared/workspace/asutame_tools/asutame_tools/tmp/input.txt'

import os
from array import array
from lzss import encode,decode

match_position = 0
match_length = 0

with open(inputFilename,'rb') as inputFile:
    inputBuffer=array('B')
    inputBuffer.fromfile(inputFile,os.stat(inputFilename).st_size)
    print encode(inputBuffer,0,os.stat(inputFilename).st_size)
    