# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/rd/content/bilan.py
# Compiled at: 2011-10-12 13:31:11
from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import form, dexterity
from ageliaco.rd import _
from plone.app.textfield import RichText
import datetime

class IBilan(form.Schema):
    """
    Bilan de projet
    """
    presentation = RichText(title=_('Présentation du bilan'), description=_('Objectifs réalisés ou à réaliser'), required=True)
    docs = schema.Text(title=_('Documents produits'), description=_('Type de document et référence'), required=True, default='Aucun')
    weblink = schema.TextLine(title=_('Lien internet'), description=_('Version internet du projet (lien principal)'), required=False)