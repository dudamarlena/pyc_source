# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/unittest/__main__.py
# Compiled at: 2018-07-11 18:15:30
"""Main entry point"""
import sys
if sys.argv[0].endswith('__main__.py'):
    sys.argv[0] = 'unittest2'
__unittest = True
from django.utils.unittest.main import main_
main_()