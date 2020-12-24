# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/recaptchawidget/validators.py
# Compiled at: 2010-04-15 12:24:16
from zope.component import getMultiAdapter
from zope.app.component.hooks import getSite
from Products.validation.interfaces.IValidator import IValidator
VALID_CAPTCHA = 'very_valid'

class CaptchaValidator(object):
    __module__ = __name__
    __implements__ = IValidator

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title
        self.description = description

    def __call__(self, value, *args, **kwargs):
        site = getSite()
        if site.REQUEST.get('captcha_is_valid') == VALID_CAPTCHA:
            return 1
        captcha = getMultiAdapter((site, site.REQUEST), name='captcha')
        if captcha.verify():
            site.REQUEST['captcha_is_valid'] = VALID_CAPTCHA
            return 1
        else:
            return 'Captcha value is not correct.'