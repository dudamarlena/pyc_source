# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/formlib.py
# Compiled at: 2008-10-10 10:14:00
"""
Some formlib adds
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.interface import implements
from zope.schema.interfaces import IURI, InvalidURI
from zope.schema import URI
from zope.app.form.browser import ASCIIWidget

class IURLLine(IURI):
    __module__ = __name__


class URLLine(URI):
    __module__ = __name__
    implements(IURLLine)

    def _validate(self, value):
        if len(value) == 0:
            return
        super(URLLine, self)._validate(value)
        if not value.startswith('http'):
            raise InvalidURI(value)


class URLWidget(ASCIIWidget):
    __module__ = __name__
    displayWidth = 80