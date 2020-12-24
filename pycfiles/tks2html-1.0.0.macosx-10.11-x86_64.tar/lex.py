# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/tks/lex.py
# Compiled at: 2016-02-17 12:34:12
"""The Lexical Analyzer of tks2html

By Leslie Zhu <pythonisland@gmail.com>

"""

class KLexical(object):
    """The basic class for Kscript lexical analyzer"""

    def __init__(self, tks_line=''):
        self.tks_line = tks_line

    def analyse(self):
        token = ''
        for char in self.tks_line:
            if char in (' ', '\t'):
                if token.strip(' |\t') != '':
                    yield token
                    token = char
                else:
                    token += char
            elif char in ('(', '{', ')', '}', '=', '+', '-', '%', '>', '<', '>=', '<=',
                          '!=', '==', ';', ',', ':'):
                yield token
                yield char
                token = ''
                continue
            elif token and token.strip(' |\t') == '':
                yield token
                token = char
            elif token in ('//', '/*', '*/'):
                yield token
                token = char
            else:
                token += char

        if token:
            yield token