# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/services.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 854 bytes
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from ScoutSuite.providers.oci.facade.base import OracleFacade
from ScoutSuite.providers.oci.resources.identity.base import Identity
from ScoutSuite.providers.oci.resources.kms.base import KMS
from ScoutSuite.providers.oci.resources.objectstorage.base import ObjectStorage
from ScoutSuite.providers.base.services import BaseServicesConfig

class OracleServicesConfig(BaseServicesConfig):

    def __init__(self, credentials=None, **kwargs):
        super(OracleServicesConfig, self).__init__(credentials)
        facade = OracleFacade(credentials)
        self.identity = Identity(facade)
        self.objectstorage = ObjectStorage(facade)
        self.kms = KMS(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'oci'