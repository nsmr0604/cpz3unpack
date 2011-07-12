#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from scriptreader import ScriptReader

class ScriptGetter(object):
    
    def __init__(self, source_filename, relation_filename, source_path, translated_path, source_encoding, translated_encoding):
        relation_file = codecs.open(relation_filename, 'r', 'utf8')
        relation = {}
        for line in relation_file:
            r = line.split('\t')
            relation[r[0]] = (r[1], int(r[2]), int(r[3].strip()))
        
        self.source_file = codecs.open(os.path.join(source_path, source_filename))
        
        if relation.has_key(source_filename):
            try:
                translated_info = relation[source_filename]
                translated_filename = os.path.join(translated_path, translated_info[0])
                print 'Adding: ' + translated_filename
                self.translated_file = codecs.open(translated_filename, 'r', translated_encoding)
                self.translated_reader = ScriptReader(self.translated_file)
                self.start_id = translated_info[1]
                self.translated_id = translated_info[2]
            except:
                pass
    
    def get_script(self, id):
        if not self.translated_file:
            return
        id = int(id)
        
        if id < self.start_id:
            return
        
        return self.translated_reader.get_line_by_id(id + self.translated_id - self.start_id)
