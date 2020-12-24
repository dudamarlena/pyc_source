# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ngi/theme/simple/interfaces.py
# Compiled at: 2011-12-14 03:16:44
from zope.interface import Interface
from zope import schema
from ngi.theme.simple import _

class IPrefForm(Interface):
    picture = schema.Bytes(title=_('Logo File'), required=False)
    footer_text = schema.Text(title=_('Enter a footer text here'), required=False)