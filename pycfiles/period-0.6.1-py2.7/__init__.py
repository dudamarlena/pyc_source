# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/period/__init__.py
# Compiled at: 2015-03-27 10:08:24
import pkg_resources
__version__ = 'unknown'
try:
    __version__ = pkg_resources.resource_string('period', 'RELEASE-VERSION').strip()
except IOError:
    __version__ = '0.0.0'

from period.main import PeriodParser, PeriodSyntax, Stack, in_period, is_holiday