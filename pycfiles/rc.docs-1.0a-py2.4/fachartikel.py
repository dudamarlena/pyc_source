# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/rc/docs/interfaces/fachartikel.py
# Compiled at: 2009-12-01 11:18:04
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from rc.docs import docsMessageFactory as _

class IFachartikel(Interface):
    """Description of the Example Type"""
    __module__ = __name__
    untertitel = schema.TextLine(title=_('Untertitel'), required=False, description=_('Untertitel des Fachartikels.'))
    aboutauthors = schema.Text(title=_('Zu den Autoren'), required=False, description=_('Zus&auml;tzliche Angaben &uuml;ber die Autoren.'))
    fabstract = schema.Text(title=_('Abstract'), required=False, description=_('Eine kurze Beschreibung.'))
    fachartikeltext = schema.Text(title=_('Fachartikel'), required=False, description=_('Fachartikel erfassen.'))