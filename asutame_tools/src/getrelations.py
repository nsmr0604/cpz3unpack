#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs
from array import array
from scriptreader import ScriptReader

source_path = ur"D:\data\workspace\asutame_text\source" + u"\\"
translated_path = ur"D:\data\workspace\asutame_text\原档" + u"\\"

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
results = {}

def get_files(dict, path_to_search, encoding):
    for filename in [os.path.join(root, afile) for root, dirs, files in os.walk(path_to_search)\
                     for afile in files if afile.rfind('.txt') == len(afile) - 4]:
        f = codecs.open(filename, 'r', encoding)
        cache = f.read()
        f.close()
        dict[filename] = cache
        
get_files(source_files, source_path, source_encoding)

for translated_filename in [os.path.join(root, afile) for root, dirs, files in os.walk(translated_path)\
               for afile in files if afile.rfind('.txt') == len(afile) - 4]:
    f = codecs.open(translated_filename, 'r', translated_encoding)
    sr = ScriptReader(f)
    lines = sr.read_lines()
    
    if len(lines) == 0:
        continue
    
    found = False
    
    for source_filename, content in source_files.iteritems():
        equal = True
        not_found = 0
        start_pos = 0
        
        for line in lines:
            
            result = content.find(line, start_pos)
            if result == -1:
                not_found += 1
                if not_found * 100 / len(lines) > 10:
                    # 5%容错
                    break
            else:
                start_pos = result
        
        if not_found * 100 / len(lines) <= 10:
            # 5%容错
            results[source_filename] = translated_filename
            found = True
#            print str(not_found * 100 / len(lines)) + " " + source_filename
            break
    if not found:
        print "ERROR:" + translated_filename + " not found"

keys = results.keys()
keys.sort()

for k in keys:
    f_s = codecs.open(k, 'r', source_encoding)
    f_t = codecs.open(results[k], 'r', translated_encoding)
    s_s = ScriptReader(f_s)
    s_t = ScriptReader(f_t)
    line_t = s_t.read_line()
    s_t.goto_line(0)
    line_s_no = s_s.find_next_target_by_source(line_t)
    line_t_no = s_t.find_next_target_by_source(line_t)
    
    print k.replace(source_path, '') + '\t' + results[k].replace(translated_path, '') + '\t' + str(line_s_no) + '\t' + str(line_t_no)


