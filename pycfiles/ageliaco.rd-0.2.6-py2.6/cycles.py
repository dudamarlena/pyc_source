# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/rd/content/cycles.py
# Compiled at: 2011-10-12 13:31:11
from five import grok
from zope import schema
from plone.directives import form, dexterity
from ageliaco.rd import _
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from zope.interface import invariant, Invalid
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
import datetime

class ICycles(form.Schema):
    """
    Cycles de Projet RD
    """
    pass