# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/themecustomizer/src/collective/themecustomizer/setuphandlers.py
# Compiled at: 2014-01-03 12:15:14
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return []