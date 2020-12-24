# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/smtplibrary.py
# Compiled at: 2010-12-12 22:28:56
import os, smtplib
from conf import settings
from logger import Logger
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def main():
    smtp = smtpInterface(settings)
    smtp.setMessageSubject('Test Message')
    smtp.setTargetSystem('beta2')
    smtp.setRecipients(settings.SMTPRECIPIENTS['testSource'])
    smtp.setMessage('This is a test message...\r\n')
    smtp.formatMessage()
    smtp.setAttachmentText(os.path.join(smtp.settings.BASE_PATH, 'emailprocessor.py'))
    try:
        print 'trying to send message'
        smtp.sendMessage()
    except:
        print 'send failed'


class smtpInterface:

    def __init__(self, settings):
        print 'SMTP Server Started'
        self.settings = settings
        self.log = Logger(settings.LOGGING_INI)

    def prompt(self, prompt):
        return raw_input(prompt).strip()

    def setTargetSystem(self, targetsystem):
        self.targetSystem = targetsystem

    def setMessageSubject(self, messageSubject):
        self.messageSubject = messageSubject

    def setMessage(self, message):
        self.message = message

    def setRecipients(self, Recipients={}):
        self.SMTPRECIPIENTS = Recipients

    def setAttachmentText(self, textfile):
        fp = open(textfile, 'r')
        att = MIMEText(fp.read())
        fp.close()
        fileNameOnly = os.path.basename(textfile)
        att.add_header('Content-Disposition', 'attachment', filename=fileNameOnly)
        self.msg.attach(att)

    def formatMessage(self):
        self.msg = MIMEMultipart()
        try:
            self.fromaddr = self.settings.SMTPSENDER
            self.toaddrs = self.SMTPRECIPIENTS['SMTPTOADDRESS']
            self.ccaddrs = self.SMTPRECIPIENTS['SMTPTOADDRESSCC']
            self.bccaddrs = self.SMTPRECIPIENTS['SMTPTOADDRESSBCC']
        except KeyError:
            self.log.logger.exception('Unable to locate an Address')

        self.log.logger.info('self.toaddrs')
        self.log.logger.info(self.toaddrs)
        self.msg['From'] = self.fromaddr
        self.msg['To'] = (', ').join(self.toaddrs)
        self.msg['CC'] = (', ').join(self.ccaddrs)
        self.msg['BCC'] = (', ').join(self.bccaddrs)
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = self.messageSubject
        self.msg.attach(MIMEText(self.message))
        self.msg.epilogue = ''

    def sendMessage(self):
        print 'ServerAddress: %s' % self.settings.SMTPSERVER
        try:
            server = smtplib.SMTP(self.settings.SMTPSERVER)
        except smtplib.socket.error:
            print "exception: socket error can't connect to smtp server"
            return
        else:
            print "no exception: can't connect to smtp server"
            return
            if self.settings.SMTPSENDERPWD != '':
                try:
                    server.login(self.settings.SMTPSENDER, self.settings.SMTPSENDERPWD)
                except smtplib.SMTPRecipientsRefused:
                    self.log.logger.exception('smtplib.SMTPRecipientsRefused')
                    if settings.DEBUG:
                        print 'SMTPRecipientsRefused'
                    return
                except smtplib.SMTPException, detail:
                    self.log.logger.exception('smtplib.SMTPException')
                    if settings.DEBUG:
                        print detail.value
                    return
                else:
                    if settings.DEBUG:
                        print 'some other type of smtp exception'
                    return

        server.set_debuglevel(0)
        self.formatMessage()
        server.sendmail(self.fromaddr, self.toaddrs, self.msg.as_string())
        server.quit()


if __name__ == '__main__':
    main()