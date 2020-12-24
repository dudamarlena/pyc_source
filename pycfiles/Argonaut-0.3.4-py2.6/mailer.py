# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/lib/mailer.py
# Compiled at: 2011-02-18 19:15:09
from turbomail import Message

def send_mail(sender, to, subject, body):
    if sender and to and subject and body:
        message = Message(author=sender, to=to, subject=subject)
        message.rich = body
        message.plain = 'This mail should be viewed in HTML.'
        try:
            message.send()
        except Exception, msg:
            if str(msg) == '[Errno 111] Connection refused':
                pass
            else:
                raise Exception