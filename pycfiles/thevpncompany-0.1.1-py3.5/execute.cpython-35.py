# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thevpncompany/test/mock/execute.py
# Compiled at: 2019-07-12 00:27:44
# Size of source mod 2**32: 179 bytes
"""

Mock for execute module

"""

class MockExecute:

    def __init__(self, rc, stdout, stderr):
        self.rc = rc
        self.stdout = stdout
        self.stderr = stderr