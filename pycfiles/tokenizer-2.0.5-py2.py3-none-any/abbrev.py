# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/villi/github/Tokenizer/src/tokenizer/abbrev.py
# Compiled at: 2019-03-27 13:01:01
"""

    Abbreviations module for tokenization of Icelandic text

    Copyright(C) 2019 Miðeind ehf.
    Original author: Vilhjálmur Þorsteinsson

    This software is licensed under the MIT License:

        Permission is hereby granted, free of charge, to any person
        obtaining a copy of this software and associated documentation
        files (the "Software"), to deal in the Software without restriction,
        including without limitation the rights to use, copy, modify, merge,
        publish, distribute, sublicense, and/or sell copies of the Software,
        and to permit persons to whom the Software is furnished to do so,
        subject to the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    
    This module reads the definition of abbreviations from the file
    Abbrev.conf, assumed to be located in the same directory (or installation
    resource library) as this Python source file.

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from threading import Lock

class ConfigError(Exception):
    pass


class Abbreviations:
    """ Wrapper around dictionary of abbreviations, initialized from the config file """
    DICT = {}
    MEANINGS = set()
    SINGLES = set()
    FINISHERS = set()
    NOT_FINISHERS = set()
    NAME_FINISHERS = set()
    _lock = Lock()

    @staticmethod
    def add(abbrev, meaning, gender, fl=None):
        """ Add an abbreviation to the dictionary. Called from the config file handler. """
        finisher = False
        not_finisher = False
        name_finisher = False
        if abbrev.endswith(b'*'):
            finisher = True
            abbrev = abbrev[0:-1]
            if not abbrev.endswith(b'.'):
                raise ConfigError(b'Only abbreviations ending with periods can be sentence finishers')
        elif abbrev.endswith(b'!'):
            not_finisher = True
            abbrev = abbrev[0:-1]
            if not abbrev.endswith(b'.'):
                raise ConfigError(b'Only abbreviations ending with periods can be marked as not-finishers')
        elif abbrev.endswith(b'^'):
            name_finisher = True
            abbrev = abbrev[0:-1]
            if not abbrev.endswith(b'.'):
                raise ConfigError(b'Only abbreviations ending with periods can be marked as name finishers')
        if abbrev.endswith(b'!') or abbrev.endswith(b'*') or abbrev.endswith(b'^'):
            raise ConfigError(b'!, * and ^ modifiers are mutually exclusive on abbreviations')
        if abbrev in Abbreviations.DICT:
            raise ConfigError((b"Abbreviation '{0}' is defined more than once").format(abbrev))
        Abbreviations.DICT[abbrev] = (
         meaning,
         0,
         gender,
         b'skst' if fl is None else fl,
         abbrev,
         b'-')
        Abbreviations.MEANINGS.add(meaning)
        if abbrev[(-1)] == b'.' and b'.' not in abbrev[0:-1]:
            Abbreviations.SINGLES.add(abbrev[0:-1])
        if finisher:
            Abbreviations.FINISHERS.add(abbrev)
        if not_finisher or name_finisher:
            Abbreviations.NOT_FINISHERS.add(abbrev)
        if name_finisher:
            Abbreviations.NAME_FINISHERS.add(abbrev)
        return

    @staticmethod
    def has_meaning(abbrev):
        return abbrev in Abbreviations.DICT

    @staticmethod
    def has_abbreviation(meaning):
        return meaning in Abbreviations.MEANINGS

    @staticmethod
    def get_meaning(abbrev):
        """ Lookup meaning of abbreviation, if available """
        if abbrev not in Abbreviations.DICT:
            return None
        else:
            return Abbreviations.DICT[abbrev][0]

    @staticmethod
    def _handle_abbreviations(s):
        """ Handle abbreviations in the settings section """
        a = s.split(b'=', 1)
        if len(a) != 2:
            raise ConfigError(b'Wrong format for abbreviation: should be abbreviation = meaning')
        abbrev = a[0].strip()
        if not abbrev:
            raise ConfigError(b'Missing abbreviation. Format should be abbreviation = meaning.')
        m = a[1].strip().split(b'"')
        par = b''
        if len(m) >= 3:
            par = m[(-1)].strip()
        gender = b'hk'
        fl = None
        if par:
            p = par.split()
            if len(p) >= 1:
                gender = p[0].strip()
            if len(p) >= 2:
                fl = p[1].strip()
        Abbreviations.add(abbrev, m[1], gender, fl)
        return

    @staticmethod
    def initialize():
        """ Read the abbreviations config file """
        with Abbreviations._lock:
            if len(Abbreviations.DICT):
                return
            from pkg_resources import resource_stream
            with resource_stream(__name__, b'Abbrev.conf') as (config):
                for b in config:
                    s = b.decode(b'utf-8')
                    ix = s.find(b'#')
                    if ix >= 0:
                        s = s[0:ix]
                    s = s.strip()
                    if not s:
                        continue
                    if s[0] == b'[':
                        if s != b'[abbreviations]':
                            raise ConfigError(b'Wrong section header')
                        continue
                    Abbreviations._handle_abbreviations(s)