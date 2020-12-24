# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rolf/Plone5/zinstance/src/medialog.markdown/medialog/markdown/behavior.py
# Compiled at: 2018-02-07 06:06:26
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel.model import Schema
from zope.i18nmessageid import MessageFactory
from medialog.markdown.widgets.widget import MarkdownFieldWidget
_ = MessageFactory('medialog.markdown')

class IMarkdownBehavior(form.Schema):
    """ A markdown text field"""
    dexteritytextindexer.searchable('bodytext')
    bodytext = schema.Text(title='Body text', description='Note: You can select text to preview, or preview all')
    form.widget(bodytext=MarkdownFieldWidget)


alsoProvides(IMarkdownBehavior, IFormFieldProvider)