# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyano/block.py
# Compiled at: 2010-11-11 18:26:40
from validate import *
from config import conf
from interface import Interface
import smtplib

class BlockInterface(Interface):
    form_html = '\n    <p>Entering an email address in the box below will ensure that no further emails will be sent to it from this remailer.</p>\n    <div>\n      <form action="PYANO_URI" method="post" >\n        <p>\n          <input name="email" value="" />\n          <input type="submit" value="Block" />\n        </p>\n      </form>\n    </div>\n'

    def validate(self):
        email = str(self.fs['email'])
        val_email(email)
        return email

    def main(self, req):
        if len(self.fs) == 0:
            if conf.remailer_addr:
                content = self.form_html.replace('PYANO_URI', str(req.uri))
            else:
                content = '<p>remailer_addr not configured</p>'
            html = self.set_html_content(conf.block_html, content)
            req.write(html)
        else:
            msg = self.process()
            req.write(self.html_success(msg, print_back=False))

    def html(self):
        return conf.block_html

    def process(self):
        email = self.validate()
        self.send_block_email(email)
        msg = 'Successfully sent request to block all emails to ' + email + '.'
        msg += ' You will receive a confirmation email shortly.'
        return msg

    def send_block_email(self, email):
        server = smtplib.SMTP(conf.remailer_mx)
        msg = 'From: %s\r\nTo: %s\r\n\r\n' % (
         email, conf.remailer_addr)
        msg += 'DESTINATION-BLOCK %s\r\n' % email
        server.sendmail(email, conf.remailer_addr, msg)
        server.quit()


def handler(req):
    return BlockInterface()(req)