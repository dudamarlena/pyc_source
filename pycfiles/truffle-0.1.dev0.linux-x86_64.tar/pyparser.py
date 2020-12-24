# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/truffle/parsers/pyparser.py
# Compiled at: 2017-07-08 20:40:15
"""
Author: Amol Kapoor
Description: Parser for .py files
"""
import ast, pywalker

class PyParser(object):
    """Python file parser."""
    FILE_TYPE = '.py'

    def __init__(self, fname, root_dir):
        self.real_fname = fname
        try:
            self.root = ast.parse(open(fname, 'r').read())
        except SyntaxError:
            print 'File %s has invalid syntax, cannot be indexed' % self.fname
            self.root = None

        fname = ('.').join(fname.split('.')[:-1])
        self.fname = fname.replace('/', '.')
        self.root_dir = root_dir.replace('/', '.')
        return

    def index_code(self):
        walker = pywalker.FileWalker(self.fname, self.root_dir)
        walker.visit(self.root)
        data = walker.get_data()
        return {'functions': data[0], 
           'variables': data[1], 
           'imported_modules': data[2], 
           'imported_from': data[3], 
           'calls': data[4]}