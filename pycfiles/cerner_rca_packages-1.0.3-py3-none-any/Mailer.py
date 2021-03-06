# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/deliveryMethod/Mailer.py
# Compiled at: 2012-04-30 15:56:18
__doc__ = '\n.. module:: Mailer\n   :platform: Unix\n   :synopsis: This module allows users to send emails from within a python script.   \n\n.. moduleauthor:: Daniel Chee\n'
import os, smtplib, logging
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate

class Mailer(object):
    """
    classdocs
    """

    def __init__(self, fromAddr, alertFromAddr, smtpServer, smtpPort, smtpUser=None, smtpPass=None):
        """
        Creates an instance of the mailer class, capable of sending emails from within python. 
        
        Args:
            fromAddr:  The From address of the email.
            
            smtpServer:  The smtp server that will be used to send the mail. 
            
            smtpPort:   The smtp port number that will be used to send the mail. 
            
            smtpUser: (ignored) The username if that particular smtp requires one. 
            
            smtpPass: (ignored) The password corresponding to smtp user, if required. 
        """
        self.logger = logging.getLogger('Mailer')
        self.fromAddr = fromAddr
        self.alertFromAddr = alertFromAddr
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        if smtpUser != 'None':
            self.smtpUser = smtpUser
        else:
            self.smtpUser = None
        if smtpPass != 'None':
            self.smtpPass = smtpPass
        else:
            self.smtpUser = None
        return

    def sendGenMail(self, toAddr, subject, body, fromAddr=None):
        """
        Sends a generic message that does not contain an attached report. 
        
        Args:
            
            toAddresses: an array containing the recipients email addresses. 
            
            subject: the subject of the email 
            
            body: the email body text.
        
        """
        if fromAddr:
            fromAddress = fromAddr
        else:
            fromAddress = self.alertFromAddr
        message = MIMEMultipart()
        message['From'] = fromAddress
        message['To'] = COMMASPACE.join(toAddr)
        message['Subject'] = subject
        message['Date'] = formatdate(localtime=True)
        message.attach(MIMEText(body))
        server = smtplib.SMTP(self.smtpServer, self.smtpPort)
        if self.smtpUser and self.smtpPass:
            server.starttls()
            server.login(self.smtpUser, self.smtpPass)
        server.sendmail(self.fromAddr, toAddr, message.as_string())
        server.quit()

    def sendMail(self, emailItem):
        """
        Sends an email based on a email item created by the ScanEventEditor
        
        Args:
        
            emailItem: The email item to be sent. 
            
        """
        message = MIMEMultipart()
        message['From'] = self.fromAddr
        message['To'] = COMMASPACE.join(emailItem.getToAddress())
        message['Subject'] = emailItem.getSubject()
        message['Date'] = formatdate(localtime=True)
        message.attach(MIMEText(emailItem.getBody()))
        for report in emailItem.reportFiles:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(report, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(report))
            message.attach(part)

        server = smtplib.SMTP(self.smtpServer, self.smtpPort)
        if self.smtpUser and self.smtpPass:
            server.starttls()
            server.login(self.smtpUser, self.smtpPass)
        server.sendmail(self.fromAddr, emailItem.getToAddress(), message.as_string())
        server.quit()

    def testEmailItem(self, emailItem):
        message = MIMEMultipart()
        message['From'] = self.fromAddr
        message['To'] = emailItem[1]
        message['Subject'] = emailItem[2]
        message['Date'] = formatdate(localtime=True)
        message.attach(MIMEText(emailItem[3]))
        try:
            server = smtplib.SMTP(self.smtpServer, self.smtpPort)
            if self.smtpUser and self.smtpPass:
                server.starttls()
                server.login(self.smtpUser, self.smtpPass)
            server.sendmail(self.fromAddr, emailItem[1], message.as_string())
        except Exception as e:
            self.logger.critical('SMTP COMMUNICATION PROBLEM')
            self.logger.critical(e)
            exit(-1)

        server.quit()


if __name__ == '__main__':
    pass