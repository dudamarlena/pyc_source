# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/facade/securitycenter.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 4740 bytes
from azure.mgmt.security import SecurityCenter
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently

class SecurityCenterFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        return SecurityCenter(self.credentials.arm_credentials, subscription_id, '')

    async def get_pricings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            pricings_list = await run_concurrently(lambda : client.pricings.list())
            if hasattr(pricings_list, 'value'):
                return pricings_list.value
            return []
        except Exception as e:
            try:
                print_exception('Failed to retrieve pricings: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_security_contacts(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda : list(client.security_contacts.list()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve security contacts: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_auto_provisioning_settings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda : list(client.auto_provisioning_settings.list()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve auto provisioning settings: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_information_protection_policies(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            scope = '/subscriptions/{}'.format(self._subscription_id)
            return await run_concurrently(lambda : list(client.information_protection_policies.list(scope=scope)))
        except Exception as e:
            try:
                print_exception('Failed to retrieve information protection policies: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_settings(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda : list(client.settings.list()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve settings: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_alerts(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda : list(client.alerts.list()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve alerts: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_compliance_results(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            scope = '/subscriptions/{}'.format(subscription_id)
            return await run_concurrently(lambda : list(client.compliance_results.list(scope=scope)))
        except Exception as e:
            try:
                print_exception('Failed to retrieve compliance results: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_regulatory_compliance_results(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            results = []
            try:
                try:
                    compliance_standards = await run_concurrently(lambda : list(client.regulatory_compliance_standards.list()))
                except Exception as e:
                    try:
                        print_exception('Failed to retrieve regulatory compliance standards: {}'.format(e))
                        return {}
                    finally:
                        e = None
                        del e

                else:
                    for standard in compliance_standards:
                        try:
                            compliance_controls = await run_concurrently(lambda : list(client.regulatory_compliance_controls.list(regulatory_compliance_standard_name=(standard.name))))
                            for control in compliance_controls:
                                control.standard_name = standard.name
                                results.append(control)

                        except Exception as e:
                            try:
                                print_exception('Failed to retrieve compliance controls: {}'.format(e))
                            finally:
                                e = None
                                del e

            finally:
                return

            return results
        except Exception as e:
            try:
                print_exception('Failed to retrieve regulatory compliance results: {}'.format(e))
                return []
            finally:
                e = None
                del e