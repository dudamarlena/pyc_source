# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/recaptchawidget/field.py
# Compiled at: 2010-04-15 12:24:16
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Storage import ReadOnlyStorage
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Field import Field
from collective.recaptchawidget.widget import CaptchaWidget

class CaptchaField(Field):
    """A field that adds a remote captcha using collective.recaptcha."""
    __module__ = __name__
    __implements__ = Field.__implements__
    _properties = Field._properties.copy()
    _properties.update({'type': 'captcha', 'widget': CaptchaWidget, 'mode': 'w', 'storage': ReadOnlyStorage(), 'validators': ('isEmpty', 'isCaptchaCorrect')})
    security = ClassSecurityInfo()
    security.declarePrivate('set')

    def set(self, *ignored, **kwargs):
        pass

    security.declarePrivate('get')

    def get(self, instance, **kwargs):
        pass

    security.declarePrivate('getRaw')

    def getRaw(self, instance, **kwargs):
        pass

    security.declarePublic('get_size')

    def get_size(self, instance):
        return 0


registerField(CaptchaField, title='Captcha', description='Display-on-edit-only field, for adding a captcha widget')