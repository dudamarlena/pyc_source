# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/kite_mail/utils.py
# Compiled at: 2015-07-05 06:41:45
# Size of source mod 2**32: 463 bytes


def help_messages(command):
    msg = {'channel': 'Name of notice channel, or id (e.g. #example, @id)', 
     'name': 'set botname', 
     'icon': 'set image url or emoji (e.g. :shachikun:)', 
     'body': 'the flag decide include mail body part. (Default: False) '}
    if msg[command]:
        return msg[command]
    else:
        return