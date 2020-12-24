# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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