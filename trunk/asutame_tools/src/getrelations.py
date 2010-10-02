#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs
from array import array
from scriptreader import ScriptReader

source_path = ur"C:\workspace\asutame_text\source\\"
translated_path = ur"C:\workspace\asutame_text\已译\\"

source_encoding = "shift-jis"
translated_encoding = "gbk"

#    得到文本和源文件名对应关系
#		将源文本全部装入一个字典
#		从已译目录中读取每一个文件
#		在源文本中找到对应的文件
#			搜索最多100句话判断这些句子是否存在
#			如果存在，判定为同一个文件
#		生成一个对应关系的字典
#		将字典存到文件中

source_files = {}
translated_files = {}

def get_files(dict, path_to_search, encoding):
    for filename in [os.path.join(root, afile) for root, dirs, files in os.walk(path_to_search)\
                   for afile in files if afile.rfind('.txt') == len(afile) - 4]:
        f = codecs.open(filename, 'r', encoding)
        print filename
        cache = f.read()
        f.close()
        dict[filename] = cache
        
get_files(source_files, source_path, source_encoding)

for filename in [os.path.join(root, afile) for root, dirs, files in os.walk(translated_path)\
               for afile in files if afile.rfind('.txt') == len(afile) - 4]:
    f = codecs.open(filename, 'r', translated_encoding)
    sr = ScriptReader(f)
    for line in sr.read_lines():
        print line
        









