# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/shortlinks/interfaces/shortlinks.py
# Compiled at: 2009-09-09 11:35:07
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from csci.shortlinks import shortlinksMessageFactory as _

class Ishortlinks(Interface):
    """Create short links"""
    __module__ = __name__
    hmac = schema.TextLine(title=_('HMAC string'), required=False, description=_('enter security string'))
    email = schema.TextLine(title=_('Email login'), required=True, description=_('email address to use as login to server'))
    action = schema.TextLine(title=_('Action'), required=True, description=_('get_or_create_hash'))
    servername = schema.TextLine(title=_('Shortlink Server'), required=True, description=_('short.example.com'))