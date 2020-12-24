# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alex/envs/purelyjs/lib/python2.7/site-packages/purelyjs/config.py
# Compiled at: 2014-04-27 15:28:58
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import re

def parse_config(filepath):
    cfg = ConfigParser()
    cfg.read(filepath)
    section_name = 'purelyjs'
    if not cfg.has_section(section_name):
        raise ValueError('No section %s found' % section_name)
    interpreters = []
    libs = []
    tests = []
    for key, value in cfg.items(section_name):
        if key == 'interpreters':
            interpreters = re.split('\\s+', value)
        if key == 'libs':
            libs = re.split('\\s+', value)
        elif key == 'tests':
            tests = re.split('\\s+', value)

    interpreters = [ e for e in interpreters if e ]
    libs = [ lib for lib in libs if lib ]
    tests = [ test for test in tests if test ]
    return (
     interpreters, libs, tests)