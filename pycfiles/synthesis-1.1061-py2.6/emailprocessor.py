# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/emailprocessor.py
# Compiled at: 2010-12-12 22:28:56
from smtplibrary import smtpInterface
from conf import settings
import os
from clssecurity import ClsSecurity

class XMLProcessorNotifier(smtpInterface):

    def __init__(self, docName, docs=[], encrypt=False):
        if encrypt:
            self.encrypt = encrypt
            self.security = ClsSecurity()
        self.mailSystem = smtpInterface(settings)
        if docName != '':
            folderName = os.path.split(docName)[0]
            self.mailSystem.setRecipients(settings.SMTPRECIPIENTS[folderName])
            self.docName = docName
        elif len(docs) > 0:
            try:
                folderName = os.path.split(docs[0])[0]
                self.mailSystem.setRecipients(settings.SMTPRECIPIENTS[folderName])
            except KeyError:
                raise

    def sendDocumentAttachment(self, Subject='Your Message Subject', Message='Message Body goes here.', attachment=None):
        self.mailSystem.setMessageSubject(Subject)
        self.mailSystem.setMessage(Message)
        self.mailSystem.formatMessage()
        for file in attachment:
            if self.encrypt:
                attachment = 'encryptdAttachment.enc'
                self.security.encryptFile(file, attachment)
            else:
                attachment = file
            print 'file: %s' % file
            self.mailSystem.setAttachmentText(attachment)

        try:
            self.sendMessage()
        except Exception, detail:
            if settings.DEBUG:
                print 'problem sending notification', detail.value
            return

    def notifyValidationFailure(self, failureMsgs=''):
        self.mailSystem.setMessageSubject('XMLDocument FAILED Validation')
        self.mailSystem.setMessage('This email is a notification that we received XML document: %s.  \r\nThis Document FAILED to Validate properly.\r\n Error is: %s' % (
         self.docName, failureMsgs))
        try:
            self.sendMessage()
        except Exception, detail:
            if settings.DEBUG:
                print 'problem sending notification', detail.value
            return

    def notifyDuplicateDocumentError(self, failureMsgs=''):
        self.mailSystem.setMessageSubject('XMLDocument Process Import FAILED')
        self.mailSystem.setMessage('This email is a notification that we received XML document: %s.  \r\nThis Document FAILED to import because it would create duplicate records in the database.\r\n Error is: %s' % (
         self.docName, failureMsgs))
        try:
            self.sendMessage()
        except Exception, detail:
            if settings.DEBUG:
                print 'problem sending notification', detail.value
            return

    def notifyValidationSuccess(self):
        self.mailSystem.setMessageSubject('Success: XMLDocument PASSED Validation')
        self.mailSystem.setMessage('This email is a notification that we received XML document: %s.  This Document PASSED Validation proprerly.' % self.docName)
        try:
            self.sendMessage()
        except Exception, detail:
            if settings.DEBUG:
                print 'problem sending notification', detail.value
            return

    def sendMessage(self):
        try:
            self.mailSystem.sendMessage()
        except Exception, detail:
            if settings.DEBUG:
                print 'problem sending notification through mail system', detail.value
            return


if __name__ == '__main__':
    msgBody = 'Test Msg'
    filesToTransfer = ['/home/user/Documents/Development/AlexandriaConsulting/repos/trunk/synthesis/OutputFiles/page.xml']
    email = XMLProcessorNotifier('', filesToTransfer, True)
    email.sendDocumentAttachment('Your report results', msgBody, filesToTransfer)