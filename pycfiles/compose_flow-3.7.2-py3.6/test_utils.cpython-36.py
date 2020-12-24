# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_utils.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 941 bytes
from unittest import TestCase
from compose_flow import utils

class RenderTestCase(TestCase):

    def test_multiple_subs_on_same_line(self, *mocks):
        env = {'JOB_NAME':'the-job', 
         'BUILD_NUMBER':'1234'}
        content = '      - /tmp/jenkins/${JOB_NAME}/${BUILD_NUMBER}:/usr/local/src/results'
        rendered = utils.render(content, env=env)
        expected = f"      - /tmp/jenkins/{env['JOB_NAME']}/{env['BUILD_NUMBER']}:/usr/local/src/results"
        self.assertEqual(expected, rendered)

    def test_get_kv(self, *mocks):
        """Ensure a single item is parsed
        """
        data = utils.get_kv('FOO=one')
        self.assertEqual(('FOO', 'one'), data)

    def test_get_kv_multiple(self, *mocks):
        """Ensure multiple items are parsed
        """
        data = utils.get_kv('FOO=one\nBAR=two', multiple=True)
        self.assertEqual([('FOO', 'one'), ('BAR', 'two')], data)