# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/feedback/browser/form.py
# Compiled at: 2009-10-26 11:39:35
from Acquisition import aq_inner
from zope import interface
from zope import schema
from zope.component import getMultiAdapter
from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget

class IReCaptchaForm(interface.Interface):
    __module__ = __name__
    name = schema.TextLine(title='Your Name', description='enter your own name here', required=True, readonly=False, default='Name')
    email = schema.TextLine(title='Your email address', description='enter your email address here', required=True, readonly=False, default=None)
    city = schema.TextLine(title='City or Town', description='enter the nearest city or town to you', required=False, readonly=False, default=None)
    country = schema.TextLine(title='Country', description='enter the country you are in', required=False, readonly=False, default=None)
    gender = schema.Choice(title='Gender', description='please select your gender', required=False, readonly=False, default=None, vocabulary=SimpleVocabulary((SimpleTerm(value=1, token='male', title='Male'), SimpleTerm(value=2, token='female', title='Female'))))
    messageTone = schema.Choice(title='What kind of comment would you like to send?', description='', required=False, readonly=False, default=None, vocabulary=SimpleVocabulary((SimpleTerm(value=1, token='oops!', title='oops!'), SimpleTerm(value=2, token='negative', title='negative'), SimpleTerm(value=3, token='positive', title='positive'))))
    messageTone = schema.Choice(title='What would you like to commment on?', description='', required=False, readonly=False, default=None, vocabulary=SimpleVocabulary((SimpleTerm(value=1, token='Website', title='Website'), SimpleTerm(value=2, token='Advertising', title='Advertising'), SimpleTerm(value=3, token='Inappropriate websites', title='Inappropriate websites'), SimpleTerm(value=4, token='Corrections', title='Corrections'), SimpleTerm(value=5, token='Problem/Error', title='Problem/Error'), SimpleTerm(value=6, token='Other', title='Other'))))
    browser = schema.Choice(title='What browser are you using?', description='', required=False, readonly=False, default=None, vocabulary=SimpleVocabulary((SimpleTerm(value=1, token='Internet Explorer', title='Internet Explorer'), SimpleTerm(value=2, token='Firefox', title='Firefox'), SimpleTerm(value=3, token='Chrome', title='Chrome'), SimpleTerm(value=4, token='Opera', title='Opera'), SimpleTerm(value=5, token='Netscape', title='Netscape'), SimpleTerm(value=6, token='Other', title='Other'))))
    message = schema.Text(title='Message', description='enter your message', required=False, readonly=False, default=None)
    captcha = schema.TextLine(title='ReCaptcha', description='', required=False)


class ReCaptcha(object):
    __module__ = __name__
    subject = ''
    captcha = ''

    def __init__(self, context):
        self.context = context


class BaseForm(form.Form):
    """ example captcha form """
    __module__ = __name__
    fields = field.Fields(IReCaptchaForm)
    fields['captcha'].widgetFactory = ReCaptchaFieldWidget

    @button.buttonAndHandler('Save')
    def handleApply(self, action):
        (data, errors) = self.extractData()
        if data.has_key('captcha'):
            captcha = getMultiAdapter((aq_inner(self.context), self.request), name='recaptcha')
            if captcha.verify(data['captcha']):
                print 'ReCaptcha validation passed.'
                mTo = 'pjdyson@gmail.com'
                mFrom = 'pdyson@cannondata.com'
                mSubj = 'Site Feedback'
                message = 'a message from your site'
                for i in data.keys():
                    message += str(i) + ': ' + str(data[i]) + '\n'

                self.context.MailHost.send(message, mTo, mFrom, mSubj)
            else:
                print 'The code you entered was wrong, please enter the new one.'


ReCaptchaForm = wrap_form(BaseForm)