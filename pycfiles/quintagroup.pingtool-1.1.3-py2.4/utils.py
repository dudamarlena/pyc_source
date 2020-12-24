# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/utils.py
# Compiled at: 2009-03-31 04:47:33
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

def getPingSites(context):
    pp = getToolByName(context, 'portal_pingtool', None)
    values = []
    if pp:
        values = tuple([ (i.Title(), i.id) for i in pp.objectValues() ])
    return SimpleVocabulary.fromItems(values)