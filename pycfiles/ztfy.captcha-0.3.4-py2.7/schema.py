# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/captcha/schema.py
# Compiled at: 2014-10-14 10:09:18
__docformat__ = 'restructuredtext'
from zope.schema.interfaces import ITextLine
from zope.interface import implements
from zope.schema import TextLine

class ICaptcha(ITextLine):
    """Captcha schema field interface"""
    pass


class Captcha(TextLine):
    """Captcha schema field"""
    implements(ICaptcha)