# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/recaptchawidget/interfaces/recaptchaedcontent.py
# Compiled at: 2010-04-15 12:24:16
from zope.interface import Interface
from zope import schema
from collective.recaptchawidget import recaptchawidgetMessageFactory as _

class IRecaptchaedContent(Interface):
    """Just some content type with a captcha"""
    __module__ = __name__
    Text = schema.Text(title=_('Text'), required=True, description=_('Field description'))