# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/modulealiases.py
# Compiled at: 2008-10-23 05:55:17
"""Module aliases for unpickling

The dotted class path of most persistent classes were changed after version 2.6
This module creates aliases using sys.modules for unpickling old objects.
"""
__author__ = ''
__docformat__ = 'restructuredtext'
import sys
from iw import fss
sys.modules['Products.FileSystemStorage'] = fss