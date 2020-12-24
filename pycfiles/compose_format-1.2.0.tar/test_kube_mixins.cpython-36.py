# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_kube_mixins.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 615 bytes
from unittest import TestCase, mock
from compose_flow.kube.mixins import KubeMixIn

class KubeMixInTestCase(TestCase):

    def test_get_secret_name_param(self, *mocks):
        """Ensure the name param is used when getting a secret
        """
        mixin = KubeMixIn()
        mixin.workflow = mock.Mock(config_name='BAD')
        mixin.namespace = 'something'
        mixin.execute = mock.Mock()
        secret_name = 'GOODNAME'
        mixin._get_secret(secret_name)
        mixin.execute.assert_called_with(f"rancher kubectl get secrets --namespace something -o yaml {secret_name}")