# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/__init__.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 487 bytes
import os
from unittest import TestCase, mock
CF_DOCKER_IMAGE_PREFIX = 'test.registry.prefix.com'
os.environ['CF_DOCKER_IMAGE_PREFIX'] = CF_DOCKER_IMAGE_PREFIX

class BaseTestCase(TestCase):

    def setUp(self):
        os.environ.pop('DOCKER_HOST', None)
        super().setUp()
        self.sh_patcher = mock.patch('compose_flow.shell.sh')
        self.sh_mock = self.sh_patcher.start()
        self.addCleanup(self.sh_patcher.stop)