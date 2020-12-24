# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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