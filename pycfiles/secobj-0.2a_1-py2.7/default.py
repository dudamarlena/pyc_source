# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/provider/default.py
# Compiled at: 2012-08-13 03:22:25
from secobj.principal import ANONYMOUS
from secobj.provider import SecurityProvider

class DefaultSecurityProvider(SecurityProvider):

    def getcurrentuser(self):
        return ANONYMOUS

    def is_subject_in_group(self, subject, group):
        return False