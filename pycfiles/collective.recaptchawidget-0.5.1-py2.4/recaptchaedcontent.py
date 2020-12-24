# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/recaptchawidget/interfaces/recaptchaedcontent.py
# Compiled at: 2010-04-15 12:24:16
from zope.interface import Interface
from zope import schema
from collective.recaptchawidget import recaptchawidgetMessageFactory as _

class IRecaptchaedContent(Interface):
    """Just some content type with a captcha"""
    __module__ = __name__
    Text = schema.Text(title=_('Text'), required=True, description=_('Field description'))