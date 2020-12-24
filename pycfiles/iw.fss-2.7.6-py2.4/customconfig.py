# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/customconfig.py
# Compiled at: 2008-10-23 05:55:17
"""
Custom config data
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import os
ZOPETESTCASE = 'ZOPE_TESTCASE' in os.environ or 'ZOPETESTCASE' in os.environ
del os
INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE = 'FSS_INSTALL_EXAMPLE_TYPES'