# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/multisitepanel/utils.py
# Compiled at: 2010-07-14 09:47:00


def getZopeRoot(context):
    return context.restrictedTraverse('/')


def getSitesList(context):
    return context.ZopeFind(getZopeRoot(context), obj_metatypes=['Plone Site'])