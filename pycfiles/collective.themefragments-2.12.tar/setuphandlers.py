# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/themecustomizer/src/collective/themecustomizer/setuphandlers.py
# Compiled at: 2014-01-03 12:15:14
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return []