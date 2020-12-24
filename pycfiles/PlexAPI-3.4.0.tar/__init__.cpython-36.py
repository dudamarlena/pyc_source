# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\geoffrey\workspace\python-plex\build\lib\plex\__init__.py
# Compiled at: 2018-02-04 13:21:25
# Size of source mod 2**32: 1167 bytes
__doc__ = '\nPython Lexical Analyser\n=======================\n\nThe Plex module provides lexical analysers with similar capabilities\nto GNU Flex. The following classes and functions are exported;\nsee the attached docstrings for more information.\n\n   Scanner          For scanning a character stream under the\n                    direction of a Lexicon.\n\n   Lexicon          For constructing a lexical definition\n                    to be used by a Scanner.\n\n   Str, Any, AnyBut, AnyChar, Seq, Alt, Opt, Rep, Rep1,\n   Bol, Eol, Eof, Empty\n\n                    Regular expression constructors, for building pattern\n                    definitions for a Lexicon.\n\n   State            For defining scanner states when creating a\n                    Lexicon.\n\n   TEXT, IGNORE, Begin\n\n                    Actions for associating with patterns when\n                    creating a Lexicon.\n'
__version__ = '2.0.0'
from plex.actions import TEXT, IGNORE, Begin
from plex.lexicons import Lexicon, State
from plex.regexps import RE, Seq, Alt, Rep1, Empty, Str, Any, AnyBut, AnyChar, Range
from plex.regexps import Opt, Rep, Bol, Eol, Eof, Case, NoCase
from plex.scanners import Scanner