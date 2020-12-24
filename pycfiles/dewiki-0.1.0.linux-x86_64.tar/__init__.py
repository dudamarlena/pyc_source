# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/dewiki/__init__.py
# Compiled at: 2013-01-12 09:33:12
"""
Created on Jan 12, 2013

@author: dirk dierickx
"""

def from_string(string=''):
    """
    Remove wiki markup text from a string
    """
    from dewiki.parser import Parser
    return Parser().parse_string(string)


def from_byte(byte=None):
    pass


def from_file(file=None):
    pass