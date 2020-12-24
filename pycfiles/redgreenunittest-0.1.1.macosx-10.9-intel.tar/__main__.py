# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/redgreenunittest/__main__.py
# Compiled at: 2013-05-11 02:09:42
"""Main entry point"""
import sys
if sys.argv[0].endswith('__main__.py'):
    sys.argv[0] = 'python -m redgreenunittest'
__unittest = True
from .main import main, TestProgram, USAGE_AS_MAIN
TestProgram.USAGE = USAGE_AS_MAIN
main(module=None)