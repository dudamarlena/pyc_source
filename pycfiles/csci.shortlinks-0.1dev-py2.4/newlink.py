# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/shortlinks/browser/newlink.py
# Compiled at: 2009-09-09 11:42:55
from zope import interface, schema
from zope.formlib import form
from Products.Five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from csci.shortlinks import shortlinksMessageFactory as _
from plone.app.form.validators import null_validator
from Products.statusmessages.interfaces import IStatusMessage
import google_short

class InewlinkSchema(interface.Interface):
    __module__ = __name__
    long_url = schema.TextLine(title='Enter URL to shorten', description='paste link here', required=True, readonly=False, default='http://')


class newlink(formbase.PageForm):
    __module__ = __name__
    form_fields = form.FormFields(InewlinkSchema)
    label = _('Create New Link')
    description = _('Create a new shortlink here')

    @form.action('Submit')
    def actionSubmit(self, action, data):
        shorturl = google_short.get_short(server=self.context.servername, action=self.context.action, hmac=self.context.hmac, email=self.context.email, url=data['long_url'], short_name='anything', is_public='true')
        shorturl = shorturl.replace('/s.14o', '/14o')
        output_str = data['long_url'] + ' is \n now ' + shorturl
        IStatusMessage(self.request).addStatusMessage(_(output_str), type='info')

    @form.action('Cancel', validator=null_validator)
    def actionCancel(self, action, data):
        self.request.response.redirect(self.context.absolute_url() + '/')