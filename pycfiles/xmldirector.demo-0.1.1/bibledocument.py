# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajung/sandboxes/xmldirector.plonecore/src/xmldirector.demo/xmldirector/demo/demo/bibledocument.py
# Compiled at: 2015-04-10 12:23:21
"""
A sample Dexterity content-type implementation using
all XML field types.
"""
from zope.interface import implements
from plone.dexterity.content import Item
from plone.supermodel import model
from xmldirector.plonecore.i18n import MessageFactory as _
from xmldirector.plonecore.dx import dexterity_base
from xmldirector.plonecore.dx.xml_field import XMLText

class IBibleDocument(model.Schema):
    xml_content = XMLText(title=_('XML Content'), required=False)


class BibleDocument(Item, dexterity_base.Mixin):
    implements(IBibleDocument)