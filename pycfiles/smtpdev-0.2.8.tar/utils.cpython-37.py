# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/projects/smtpdev/smtpdev/utils.py
# Compiled at: 2019-06-01 07:45:56
# Size of source mod 2**32: 445 bytes
from smtplib import SMTP
from typing import List
default_body = '\nFrom: John Doe <jdoe@example.com>\nTo: Jane Doe <janed@example.com>\nSubject: Hello!\n\nHi, Jane, this is me!\n'

def send_test_email(host: str, port: int, from_: str='sender@example.com', to: List[str]=None, body: str=None):
    to = to or ['recipient@example.com']
    body = body or default_body
    client = SMTP(host, port)
    client.sendmail(from_, to, body)