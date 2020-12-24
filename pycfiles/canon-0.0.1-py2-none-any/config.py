# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/canoe/config/config.py
# Compiled at: 2013-03-20 10:50:18
from parser import parser
from lex import lexer

class Config(object):

    def __init__(self, watches):
        self.watching = watches

    @classmethod
    def from_file(cls, file):
        config = None
        env = {}
        with open(file) as (f):
            inp = f.read()
            cn = parser.parse(inp, lexer=lexer)
            config = cn.evaluate(env)
        return config