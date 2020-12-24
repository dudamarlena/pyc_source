# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/test_pre_commit_normalization.py
# Compiled at: 2019-03-02 08:33:11
# Size of source mod 2**32: 718 bytes
import subprocess, unittest

class TestPreCommitNormalization(unittest.TestCase):

    def test_normalization(self):
        """ We test if the code was properly formatted with pre-commit. """
        pre_commit_command = [
         'pre-commit', 'run', '--all-files']
        try:
            subprocess.check_call(pre_commit_command)
        except subprocess.CalledProcessError:
            msg = 'You did not apply pre-commit hook to your code, or you did not fix all the problems. We launched pre-commit during tests but there might still be some warnings or errorsto silence with pragma.'
            self.fail(msg)

        self.assertTrue(True)