# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/acm.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1194 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import map_concurrently, run_concurrently

class AcmFacade(AWSBaseFacade):

    async def get_certificates(self, region):
        try:
            cert_list = await AWSFacadeUtils.get_all_pages('acm', region, self.session, 'list_certificates', 'CertificateSummaryList')
            cert_arns = [cert['CertificateArn'] for cert in cert_list]
        except Exception as e:
            try:
                print_exception('Failed to get acm certificates: {}'.format(e))
                return []
            finally:
                e = None
                del e

        else:
            return await map_concurrently((self._get_certificate), cert_arns, region=region)

    async def _get_certificate(self, cert_arn: str, region: str):
        client = AWSFacadeUtils.get_client('acm', self.session, region)
        try:
            return await run_concurrently(lambda : client.describe_certificate(CertificateArn=cert_arn)['Certificate'])
        except Exception as e:
            try:
                print_exception('Failed to describe acm certificate: {}'.format(e))
                raise
            finally:
                e = None
                del e