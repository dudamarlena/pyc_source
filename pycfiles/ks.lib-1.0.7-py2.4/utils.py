# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/lib/datetime/utils.py
# Compiled at: 2008-10-21 04:34:39
"""datetime utils for the Zope 3 based ks.lib.datetime package

$Id: utils.py 35252 2007-12-03 18:46:05Z anatoly $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 35252 $'
__date__ = '$Date: 2007-12-03 20:46:05 +0200 (Mon, 03 Dec 2007) $'
import datetime

def timedelta2seconds(value):
    assert isinstance(value, datetime.timedelta)
    return value.days * 24 * 3600 + value.seconds + value.microseconds