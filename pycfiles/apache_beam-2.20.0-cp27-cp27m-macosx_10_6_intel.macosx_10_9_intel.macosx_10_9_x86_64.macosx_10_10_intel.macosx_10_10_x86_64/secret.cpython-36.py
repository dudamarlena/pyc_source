# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/kubernetes/secret.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2727 bytes
from airflow.exceptions import AirflowConfigException

class Secret(object):
    """Secret"""

    def __init__(self, deploy_type, deploy_target, secret, key=None):
        """Initialize a Kubernetes Secret Object. Used to track requested secrets from
        the user.
        :param deploy_type: The type of secret deploy in Kubernetes, either `env` or
            `volume`
        :type deploy_type: str
        :param deploy_target: (Optional) The environment variable when
            `deploy_type` `env` or file path when `deploy_type` `volume` where
            expose secret. If `key` is not provided deploy target should be None.
        :type deploy_target: str or None
        :param secret: Name of the secrets object in Kubernetes
        :type secret: str
        :param key: (Optional) Key of the secret within the Kubernetes Secret
            if not provided in `deploy_type` `env` it will mount all secrets in object
        :type key: str or None
        """
        self.deploy_type = deploy_type
        self.deploy_target = deploy_target
        if deploy_target is not None:
            if deploy_type == 'env':
                self.deploy_target = deploy_target.upper()
        if key is not None:
            if deploy_target is None:
                raise AirflowConfigException('If `key` is set, `deploy_target` should not be None')
        self.secret = secret
        self.key = key

    def __eq__(self, other):
        return self.deploy_type == other.deploy_type and self.deploy_target == other.deploy_target and self.secret == other.secret and self.key == other.key

    def __repr__(self):
        return 'Secret({}, {}, {}, {})'.format(self.deploy_type, self.deploy_target, self.secret, self.key)