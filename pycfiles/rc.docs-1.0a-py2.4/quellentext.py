# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/rc/docs/interfaces/quellentext.py
# Compiled at: 2009-11-17 12:40:42
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from rc.docs import docsMessageFactory as _

class IQuellentext(Interface):
    """Quellentext zum Projekt einfügen"""
    __module__ = __name__
    fundort = schema.TextLine(title=_('Fundort'), required=False, description=_('ID oder String'))
    druckort = schema.TextLine(title=_('Druckort'), required=False, description=_('ID oder String'))
    regest = schema.Text(title=_('Regest'), required=False, description=_('Kurzbeschreibung eingeben.'))
    originaltext = schema.Text(title=_('Originaltext'), required=False, description=_('Text erfassen.'))
    kommentar = schema.Text(title=_('Kommentar'), required=False, description=_('Kommentare zum Artikel eingeben.'))