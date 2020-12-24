# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/twitter/browser/addtweet.py
# Compiled at: 2009-08-10 05:45:05
from zope import interface, schema
from zope.formlib import form
from Products.Five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from wwp.twitter import twitterMessageFactory as _
import twitter
from plone.app.form.validators import null_validator
from Products.statusmessages.interfaces import IStatusMessage

class IaddtweetSchema(interface.Interface):
    __module__ = __name__
    tweettext = schema.Text(title='Enter tweet to post', description='Max 140 characters', required=True, readonly=False, default=None)

    @interface.invariant
    def invariant_checklength(input):
        if len(input.tweettext) > 140:
            raise interface.Invalid('Set either title or subtitle.')


class addtweet(formbase.PageForm):
    __module__ = __name__
    form_fields = form.FormFields(IaddtweetSchema)
    label = _('Add Tweet')
    description = _('Add tweet to twitter')

    @form.action('Submit')
    def actionSubmit(self, action, data):
        if self.context.password == '':
            IStatusMessage(self.request).addStatusMessage(_('Password not set! Cannot post'), type='error')
            return
        api = twitter.Api(username=self.context.username, password=self.context.password)
        statuses = api.PostUpdate(status=data['tweettext'], in_reply_to_status_id=None)
        self.request.response.redirect(self.context.absolute_url() + '/')
        return

    @form.action('Cancel', validator=null_validator)
    def actionCancel(self, action, data):
        self.request.response.redirect(self.context.absolute_url() + '/')