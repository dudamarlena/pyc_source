# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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