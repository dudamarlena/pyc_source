# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/App/Validation/Automation/alarming.py
# Compiled at: 2012-05-02 12:24:07
import smtplib, logging

class Alarming:
    """ Notifies of a potential issue via email and/or text message.The
        recipient(s) address is a part of the configuration file.
    """
    __module__ = __name__

    def __init__(self):
        self.config = {}
        self.data = {}

    def mail(self, mail_from, mail_to, smtp, subject, body):
        """ Sends email notification about the exception encountered while
            performing validation.

            >>> auto_obj  = Alarming()
            >>> hostname  = socket.getfqdn()
            >>> user      = os.environ['USER']
            >>> mail_from = user+'@'+hostname
            >>> mail_to   = user+'@'+hostname
            >>> auto_obj.mail(mail_from, mail_to, hostname, "test", "test")
            True
        """
        try:
            server = smtplib.SMTP(smtp)
            server.sendmail(mail_from, mail_to, body)
            server.quit()
        except smtplib.SMTPException, err:
            logger = logging.getLogger(__name__)
            logger.error('Email sending failed :ERROR:' + str(err) + '\n')
            self.data['MAIL_MSG'] = str(err)
            return False

        self.data['MAIL_MSG'] = '\nMail sent to ' + mail_to + ' with content:\n' + body + '\n'
        return True

    def page(self, mail_from, mail_to, smtp, subject, body):
        """ Sends page notification about the exception encountered while
            performing validation.

            >>> auto_obj  = Alarming()
            >>> hostname  = socket.getfqdn()
            >>> user      = os.environ['USER']
            >>> mail_from = user+'@'+hostname
            >>> mail_to   = user+'@'+hostname
            >>> auto_obj.page(mail_from, mail_to, hostname, "test", "test")
            True
        """
        try:
            server = smtplib.SMTP(smtp)
            server.sendmail(mail_from, mail_to, body)
            server.quit()
        except smtplib.SMTPException, err:
            logger = logging.getLogger(__name__)
            logger.error('Page sending failed :ERROR:' + str(err) + '\n')
            self.data['PAGE_MSG'] = str(err)
            return False

        self.data['PAGE_MSG'] = '\nPage sent to ' + mail_to + ' with the\t\t\t\t      following content:\n' + body + '\n'
        return True


if __name__ == '__main__':
    import doctest, socket, os
    doctest.testmod()