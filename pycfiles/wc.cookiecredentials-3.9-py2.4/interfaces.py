# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/cookiecredentials/interfaces.py
# Compiled at: 2007-09-20 06:47:27
from zope.interface import Interface
from zope.schema import ASCIILine
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('wc.cookiecredentials')

class ICookieCredentials(Interface):
    __module__ = __name__
    cookie_name = ASCIILine(title=_('Cookie name'), description=_('Name of the cookie for storing credentials.'), required=True)