#!/usr/bin/env python

class AndroidClassGenerator(object):
    
    def __init__(self):
        self.string_attrs = []
        self.file_name = None
        
    def create_file(self):
        text  = self.header_string()
        text += '\n\n'
        text += self.class_string()
        
        body = ''
        for string_attr in self.string_attrs:
            body += getattr(self, string_attr)()
            body += '\n\n'
        
        with open(self.file_name, 'w') as fout:
            fout.write(text % (body))
            
    def header_string(self):
        raise NotImplementedError
        
    def class_string(self):
        raise NotImplementedError
