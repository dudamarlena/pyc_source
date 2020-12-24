# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/locale/test_locale_normalization.py
# Compiled at: 2020-02-23 10:00:28
# Size of source mod 2**32: 1490 bytes
import os, platform, subprocess, unittest
from pathlib import Path

class TestLocaleNormalization(unittest.TestCase):
    LOCALE_PATH = Path('survey', 'locale').absolute()

    def test_normalization(self):
        """ We test if the messages were properly created with makemessages --no-obsolete --no-wrap. """
        if platform.system() == 'Windows':
            python_3 = [
             'py', '-3']
        else:
            python_3 = [
             'python3']
        makemessages_command = python_3 + [
         'manage.py',
         'makemessages',
         '--no-obsolete',
         '--no-wrap',
         '--ignore',
         'venv']
        number_of_language = len(os.listdir(self.LOCALE_PATH))
        subprocess.check_call(makemessages_command)
        git_diff_command = ['git', 'diff', self.LOCALE_PATH]
        git_diff = subprocess.check_output(git_diff_command).decode('utf8')
        number_of_change = git_diff.count('@@') / 2
        msg = (
         "You did not update the translation following your changes. Maybe you did not use the normalized 'python3 manage.py makemessages --no-obsolete --no-wrap' ? If you're working locally, just use 'git add {}', we launched it during tests.".format(self.LOCALE_PATH),)
        self.assertEqual(number_of_change, number_of_language, msg)