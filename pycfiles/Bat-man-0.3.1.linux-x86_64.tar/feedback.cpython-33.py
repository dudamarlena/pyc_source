# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/feedback.py
# Compiled at: 2014-02-04 19:25:36
# Size of source mod 2**32: 423 bytes
import subprocess
try:
    subprocess.call(['xdg-email', '--version'], stdout=subprocess.DEVNULL)
except (OSError, FileNotFoundException):
    raise RuntimeError("Couldn't find xdg-email, needed for feedback module")

DESTINATION = 'ramon100.black@gmail.com'
SUBJECT = 'Bat-man feedback'

def open_email_sender_for_feedback():
    subprocess.call(['xdg-email', '--subject', SUBJECT, DESTINATION])