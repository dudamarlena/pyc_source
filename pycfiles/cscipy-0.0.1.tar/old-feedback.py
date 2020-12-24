# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/feedback/browser/old-feedback.py
# Compiled at: 2009-10-26 10:49:24
from zope import interface, schema
from zope.formlib import form
from Products.Five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from csci.feedback import feedbackMessageFactory as _
from zope.interface import invariant, Invalid
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget

def val_captcha(value):
    print 'validating: ', value
    result = True
    return result


class IfeedbackSchema(interface.Interface):
    __module__ = __name__
    name = schema.TextLine(title='Your Name', description='enter your own name here', required=True, readonly=False, default='Name')
    email = schema.TextLine(title='Your email address', description='enter your email address here', required=True, readonly=False, default=None)
    city = schema.TextLine(title='City or Town', description='enter the nearest city or town to you', required=False, readonly=False, default=None)
    country = schema.TextLine(title='Country', description='enter the country you are in', required=False, readonly=False, default=None)
    gender = schema.Choice(title='Gender', description='please select your gender', required=False, readonly=False, default=None, vocabulary=SimpleVocabulary((SimpleTerm(value=1, token='male', title='Male'), SimpleTerm(value=2, token='female', title='Female'))))
    captcha = schema.TextLine(title='Captcha', description='', required=True, readonly=False, default=None)


class ReCaptcha(object):
    __module__ = __name__
    subject = ''
    captcha = ''

    def __init__(self, context):
        self.context = context


class feedback(formbase.PageForm):
    __module__ = __name__
    form_fields = form.FormFields(IfeedbackSchema)
    form_fields['captcha'].widgetFactory = ReCaptchaFieldWidget
    label = _('Feedback Form')
    description = _('Contact us and leave feedback')

    @form.action('Submit')
    def actionSubmit(self, action, data):
        pass

    @form.action('Cancel')
    def actionCancel(self, action, data):
        pass