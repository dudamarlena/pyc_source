# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/igwtools/version.py
# Compiled at: 2008-03-25 13:06:53
from pkg_resources import get_distribution
distribution = get_distribution('igwtools')
__version__ = distribution.version