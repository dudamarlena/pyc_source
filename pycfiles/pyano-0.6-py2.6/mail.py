# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyano/mail.py
# Compiled at: 2010-11-11 17:05:59
from validate import *
from config import conf
from interface import MixInterface
from mix import send_mail

class MailInterface(MixInterface):
    form_html = '\n    <form action="PYANO_URI" method="post" >\n    <table id="mixtable">\n      <tr id="to">\n        <td><strong>*To:</strong></td>\n        <td><input class="line" name="to" value="" /></td>\n      </tr>\n      <tr id="from">\n        <td><strong>From:</strong></td>\n        <td><input class="line" name="from" value="" /></td>\n      </tr>\n      <tr id="subject">\n        <td><strong>Subject:</strong></td>\n        <td><input class="line" name="subject" value="" /></td>\n      </tr>PYANO_CHAIN\n      <tr id="copies">\n         <td><strong>Copies:</strong></td>\n         <td>\n           PYANO_COPIES\n         </td>\n      </tr>\n      <tr id="message">\n        <td><strong>*Message:</strong></td>\n        <td><textarea name="message" rows="30" cols="70" ></textarea></td>\n      </tr>\n      <tr id="buttons">\n        <td></td>\n        <td><input type="submit" value="Send" /><input type="reset" value="Reset" /></td>\n      </tr>\n    </table>\n    </form>\n'

    def validate(self):
        to = str(self.fs['to'])
        val_email(to)
        orig = str(self.fs['from'])
        if orig:
            val_email(orig)
        subj = str(self.fs['subject'])
        chain = parse_chain(self.fs)
        n_copies = int(self.fs['copies'])
        val_n_copies(n_copies)
        msg = str(self.fs['message'])
        if not msg:
            raise InputError('Refusing to send empty message.')
        return (
         to, orig, subj, chain, n_copies, msg)

    def html(self):
        return conf.mail_html

    def form(self):
        return conf.mail_form_html.replace('<!--FORM-->', MailInterface.form_html)

    def process(self):
        (to, orig, subj, chain, n_copies, msg) = self.validate()
        send_mail(to, orig, subj, chain, n_copies, msg)
        msg = 'Successfully sent message to ' + to + ' using '
        if chain:
            msg += 'remailer chain ' + (',').join(chain) + '.'
        else:
            msg += 'a random remailer chain.'
        return msg


def handler(req):
    return MailInterface()(req)