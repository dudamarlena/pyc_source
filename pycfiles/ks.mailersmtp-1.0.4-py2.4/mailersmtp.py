# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/mailersmtp/mailersmtp.py
# Compiled at: 2008-12-23 09:46:25
"""Mailer class for the Zope 3 based mailer package

$Id: mailersmtp.py 35356 2008-12-23 14:46:10Z anatoly $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 35356 $'
__date__ = '$Date: 2008-12-23 16:46:10 +0200 (Tue, 23 Dec 2008) $'
from persistent import Persistent
from zope.component import getUtility
from zope.interface import implements
from zope.app.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty
from ks.lib.mailtemplate import mailtemplate
from ks.mailer.interfaces import ITemplate, ITemplateAdaptable
from ks.mailer.templateadapter import getTemplate
from zope.i18n import translate
from ks.adapter.lazyrequest.interfaces import ILazyRequest
from interfaces import IMailerSMTP

class MailerSMTP(Persistent, Contained):
    __module__ = __name__
    implements(IMailerSMTP)
    template = FieldProperty(IMailerSMTP['template'])
    use_container = FieldProperty(IMailerSMTP['use_container'])
    use_alternative = FieldProperty(IMailerSMTP['use_alternative'])
    mime = FieldProperty(IMailerSMTP['mime'])
    filename = FieldProperty(IMailerSMTP['filename'])
    mail_header = FieldProperty(IMailerSMTP['mail_header'])
    mail_footer = FieldProperty(IMailerSMTP['mail_footer'])
    Subject = FieldProperty(IMailerSMTP['Subject'])

    def execute(self, **kw):
        if kw.has_key('attaches'):
            attaches = kw['attaches']
            del kw['attaches']
        else:
            attaches = ()
        return mailtemplate.template(use_container=self.use_container, use_alternative=self.use_alternative, charset='utf-8', mime=self.mime, filename=self.filename, mail_header=self.mail_header.encode('utf-8'), mail_footer=self.mail_footer.encode('utf-8'), attaches=attaches, text_headers={'Subject': translate(self.Subject, context=ILazyRequest(self)).encode('utf-8')}, data=kw, mail_body=getTemplate(self.template, self)(**kw).encode('utf-8'))