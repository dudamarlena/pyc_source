# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/flake8_blind_except.py
# Compiled at: 2016-06-27 15:15:47
try:
    import pycodestyle
except ImportError:
    import pep8 as pycodestyle

import re
__version__ = '0.1.1'
BLIND_EXCEPT_REGEX = re.compile('(except:)')

def check_blind_except(physical_line):
    if pycodestyle.noqa(physical_line):
        return
    match = BLIND_EXCEPT_REGEX.search(physical_line)
    if match:
        return (match.start(), 'B901 blind except: statement')


check_blind_except.name = 'flake8-blind-except'
check_blind_except.version = __version__