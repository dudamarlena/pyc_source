# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/services/mail/mailService.py
# Compiled at: 2010-06-01 14:13:33
import yaml, email, smtplib
from dust.core.util import encodeAddress

class MailHandler:

    def __init__(self):
        f = open('config/emailServer.yaml', 'r')
        self.config = yaml.load(f.read())
        f.close()

    def handle(self, msock, msg, addr):
        print('-----------------')
        print(msg.decode('ascii'))
        msg = msg.decode('ascii')
        mail = email.message_from_string(msg)
        to = mail['To']
        frm = mail['From']
        print('To:', to, 'From:', frm)
        tod = to.split('@')[1]
        frmd = frm.split('@')[1]
        addressKey = encodeAddress(addr)
        try:
            sender = self.config['senders'][addressKey]
        except:
            print('Unknown sender', addr, 'trying generic...')
            try:
                sender = self.config['senders']['*']
            except:
                print('No generic sender rules, rejecting.')
                return

        if tod not in sender['to']:
            print('Illegal to address', tod, sender['to'])
        else:
            if frmd not in sender['from']:
                print('Illegal from address', frmd, sender['from'])
            else:
                print('Sending...')