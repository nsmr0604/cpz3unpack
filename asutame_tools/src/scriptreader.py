#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ScriptReader(object):
    def __init__(self, script_file):
        '''
        一个file对象
        '''
        self.script_file = script_file
        
    def read_lines(self):
        '''
        返回所有行组成的列表
        '''
        result = []
        while True:
            line = self.read_line()
            if line == '':
                return result
            result.append(line)
        return result

    def read_id_and_line(self):
        '''
        读取下一行
        '''
        while True:
            line = self.script_file.readline()
            if line == '':
                return ''
            
            if line[0] == ';' or len(line.rstrip()) == 0 or line.find('=') == -1:
                continue
            id_content = line.split('=')
            return (id_content[0], id_content[1].rstrip())
        return None

    def read_line(self):
        '''
        读取下一行
        '''
        r = self.read_id_and_line()
        if r:
            return r[1]
        return ''
    
    def goto_line(self, lineno):
        '''
        跳到指定的行数
        '''
        self.script_file.seek(0)
        for i in xrange(0, lineno):
            self.script_file.readline()
    
    def find_next_target_by_source(self, search):
        '''
        在当前位置之后根据未翻译的源文本查找第一处已翻译的文本，返回(\d+)=search的\d+
        '''
        while True:
            r = self.read_id_and_line()
            if r:
                if r[1] == search:
                    return int(r[0])
            else:
                return None
