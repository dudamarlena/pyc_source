# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/info/emailControl.py
# Compiled at: 2007-12-02 16:26:59
from salamoia.h2o.object import Object
from email.Message import Message
from email.Parser import *
from salamoia.h2o.template import *
from salamoia.h2o.logioni import *
from salamoia.h2o.exception import *
from salamoia.h2o.container import *
from smtplib import *
from salamoia.nacl.info.sendmail import sendmail
from salamoia.nacl.backend import *
import os

class MailControl(object):
    __module__ = __name__

    def __init__(self, filename='Mail.db'):
        super(MailControl, self).__init__()
        varPath = NACLBackend.defaultBackend().varPath()
        self.engine = TemplateEngine(varPath, filename)

    def getMail(self, user, key):
        mails = self.engine.get(user)
        return Container(mails[key])

    def addMail(self, user, mail, mailKey='Subject'):
        key = mail[mailKey]
        try:
            mails = self.engine.get(user)
            mails[key] = mail
            self.engine.add(user, mails)
        except:
            mails = {}
            mails[key] = mail
            self.engine.add(user, mails)

        return 1

    def delMail(self, user, key):
        Ione.log('deleting mail for', user, key)
        mails = self.engine.get(user)
        del mails[key]
        self.engine.add(user, mails)
        return 1

    def listMail(self, user):
        try:
            mails = self.engine.get(user).keys()
        except:
            mails = []

        return Container(mails)

    def send(self, mail):
        return sendmail(mail)


from salamoia.tests import *
runDocTests()