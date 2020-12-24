# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/provider.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1348 bytes
import os
from ScoutSuite.providers.oci.services import OracleServicesConfig
from ScoutSuite.providers.base.provider import BaseProvider

class OracleProvider(BaseProvider):
    __doc__ = '\n    Implements provider for Azure\n    '

    def __init__(self, report_dir=None, timestamp=None, services=None, skipped_services=None, **kwargs):
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services
        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]
        self.provider_code = 'oci'
        self.provider_name = 'Oracle Cloud Infrastructure'
        self.environment = 'default'
        self.services_config = OracleServicesConfig
        self.credentials = kwargs['credentials']
        self.account_id = self.credentials.get_scope()
        super(OracleProvider, self).__init__(report_dir, timestamp, services, skipped_services)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        if self.account_id:
            return 'oracle-{}'.format(self.account_id)
        return 'oracle'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        super(OracleProvider, self).preprocessing()