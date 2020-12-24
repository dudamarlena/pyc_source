# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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