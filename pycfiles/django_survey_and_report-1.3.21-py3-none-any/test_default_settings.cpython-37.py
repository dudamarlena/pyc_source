# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/test_default_settings.py
# Compiled at: 2020-02-05 17:38:32
# Size of source mod 2**32: 547 bytes
from django.conf import settings
from django.test import override_settings
from survey import set_default_settings
from survey.tests import BaseTest

@override_settings()
class TestDefaultSettings(BaseTest):

    def test_set_choices_separator(self):
        url = '/admin/survey/survey/1/change/'
        del settings.CHOICES_SEPARATOR
        self.login()
        set_default_settings()
        try:
            self.client.get(url)
        except AttributeError:
            self.fail('AttributeError: survey failed to set CHOICES_SEPARATOR')