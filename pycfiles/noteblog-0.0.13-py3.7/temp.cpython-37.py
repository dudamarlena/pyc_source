# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/brush/temp.py
# Compiled at: 2019-05-05 08:03:50
# Size of source mod 2**32: 605 bytes
from time import time, sleep
from fzutils import TwentyFourEmail
_ = TwentyFourEmail()
email_address = _._get_email_address()
print('获取到的email_address: {}'.format(email_address))
message_count = lambda : _._get_email_message_count()
start_time = time()
index = 1
while message_count() in (0, None) and time() - start_time < 100.0:
    sleep_time = 2
    print('{} try, 休眠{}s...'.format(index, sleep_time))
    sleep(sleep_time)
    index += 1

message_list = _._get_email_message_list()
print(message_list)