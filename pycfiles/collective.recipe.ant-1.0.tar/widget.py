# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/recaptchawidget/widget.py
# Compiled at: 2010-04-15 12:24:16
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget
from AccessControl import ClassSecurityInfo

class CaptchaWidget(TypesWidget):
    __module__ = __name__
    _properties = TypesWidget._properties.copy()
    _properties.update({'macro': 'recaptchawidget'})
    security = ClassSecurityInfo()


registerWidget(CaptchaWidget, title='Captcha', description='Renders a captcha from collective.recaptcha', used_for=('Products.Archetypes.Field.CaptchaField', ))