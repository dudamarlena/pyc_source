# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/base/log.py
# Compiled at: 2020-02-26 14:47:57
# Size of source mod 2**32: 254 bytes
from django.utils.log import AdminEmailHandler

class CustomAdminEmailHandler(AdminEmailHandler):

    def format_subject(self, subject):
        subject = subject.split('\n')[0]
        return super(CustomAdminEmailHandler, self).format_subject(subject)