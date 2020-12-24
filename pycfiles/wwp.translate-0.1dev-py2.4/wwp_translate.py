# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/translate/interfaces/wwp_translate.py
# Compiled at: 2009-07-27 11:24:53
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from wwp.translate import translateMessageFactory as _

class Iwwp_translate(Interface):
    """Translation of text to and from different languages"""
    __module__ = __name__
    to_lang = schema.TextLine(title=_('To language'), required=True, description=_('Translate to this language'))
    from_lang = schema.TextLine(title=_('From language'), required=True, description=_('translate from this language'))