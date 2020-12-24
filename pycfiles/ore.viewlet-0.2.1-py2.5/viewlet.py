# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/viewlet/viewlet.py
# Compiled at: 2008-05-19 13:01:22
"""
$Id: viewlet.py 1965 2007-05-22 03:41:22Z hazmat $
"""
from zope.app.annotation.interfaces import IAnnotations
from zope.interface import implements
from zope import schema
from persistent.dict import PersistentDict
from zope.schema.interfaces import IContextSourceBinder, IIterableSource
from zope.schema.vocabulary import SimpleVocabulary
from Products.Five.formlib.formbase import FormBase, SubPageForm
from Products.CMFCore.utils import getToolByName
from interfaces import IViewComponent