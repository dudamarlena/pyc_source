# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/iam/credentialreports.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1854 bytes
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id

class CredentialReports(AWSResources):

    async def fetch_all(self):
        raw_credential_reports = await self.facade.iam.get_credential_reports()
        for raw_credential_report in raw_credential_reports:
            name, resource = self._parse_credential_reports(raw_credential_report)
            self[name] = resource

    def _parse_credential_reports(self, raw_credential_report):
        user_id = raw_credential_report['user']
        raw_credential_report['name'] = user_id
        raw_credential_report['id'] = user_id
        raw_credential_report['password_last_used'] = self._sanitize_date(raw_credential_report['password_last_used'])
        raw_credential_report['access_key_1_last_used_date'] = self._sanitize_date(raw_credential_report['access_key_1_last_used_date'])
        raw_credential_report['access_key_2_last_used_date'] = self._sanitize_date(raw_credential_report['access_key_2_last_used_date'])
        raw_credential_report['last_used'] = self._compute_last_used(raw_credential_report)
        return (get_non_provider_id(user_id), raw_credential_report)

    @staticmethod
    def _sanitize_date(date):
        """
        Returns the date if it is not equal to 'N/A' or 'no_information', else returns None
        """
        if date != 'no_information':
            if date != 'N/A':
                return date

    @staticmethod
    def _compute_last_used(credential_report):
        dates = [credential_report['password_last_used'],
         credential_report['access_key_1_last_used_date'],
         credential_report['access_key_2_last_used_date']]
        dates = [date for date in dates if date is not None]
        if len(dates) > 0:
            return max(dates)