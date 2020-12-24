# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hnc\tools\smtplogging.py
# Compiled at: 2013-01-23 05:08:42
import logging, logging.handlers

class TlsSMTPHandler(logging.handlers.SMTPHandler):

    def emit(self, record):
        """
        Emit a record.
 
        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib, string
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time

            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = 'From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s' % (
             self.fromaddr,
             string.join(self.toaddrs, ','),
             self.getSubject(record),
             formatdate(), msg)
            if self.username:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)