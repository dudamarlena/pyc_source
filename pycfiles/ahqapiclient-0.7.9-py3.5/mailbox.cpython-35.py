# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/mailbox.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 1450 bytes
from base64 import b64encode
from ahqapiclient.resources import Resource

class Mailbox(Resource):

    def __init__(self, http_client):
        super(Mailbox, self).__init__('/mailboxes', http_client)

    def create_mailbox(self, mailbox):
        return self.post(path=self.rurl(), data={'mailbox': mailbox})

    def get_mailbox(self, mailbox):
        return self.get(path=self.rurl(b64encode(mailbox)))

    def delete_mailbox(self, mailbox):
        return self.delete(path=self.rurl(b64encode(mailbox)))

    def get_mailboxes(self, raw=False):
        return self.get(path=self.rurl(), raw=raw)

    def expunge_mailbox(self, mailbox):
        return self.post(path=self.rurl('%s/expunge' % b64encode(mailbox)))

    def create_mail(self, mailbox, value, flags):
        if type(value) != unicode:
            value = unicode(value, encoding='utf-8')
        return self.post(path=self.rurl(b64encode(mailbox)), data={'value': value, 'flags': flags})

    def get_mails(self):
        pass

    def get_mail(self, mailbox, uid):
        return self.get(path=self.rurl('%s/%s' % (b64encode(mailbox), uid)))

    def update_mail(self, mailbox, uid, flags, value):
        mailbox = b64encode(mailbox)

    def delete_mail(self, mailbox, uid):
        return self.delete(path='%s/%s' % (b64encode(mailbox), uid))