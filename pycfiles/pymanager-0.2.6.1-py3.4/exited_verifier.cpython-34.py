# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/utils/exited_verifier.py
# Compiled at: 2015-03-27 17:46:03
# Size of source mod 2**32: 447 bytes
import subprocess
from .verifier import Verifier

class ExitedVerifier(Verifier):

    def __init__(self, **kwargs):
        self.timeout = 30
        self.expect_code = 0
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
        if 'expect_code' in kwargs:
            self.expect_code = kwargs['expect_code']

    def run(self, proc):
        try:
            proc.wait(self.timeout)
        except subprocess.TimeoutExpired:
            return False

        return proc.returncode == self.expect_code