# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/models/test_response.py
# Compiled at: 2019-03-02 04:44:34
# Size of source mod 2**32: 221 bytes
from survey.tests.models import BaseModelTest

class TestResponse(BaseModelTest):

    def test_unicode(self):
        """ Unicode generation. """
        self.assertIsNotNone(str(self.response))