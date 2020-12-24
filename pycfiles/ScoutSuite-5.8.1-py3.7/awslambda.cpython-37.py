# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/awslambda.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 525 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils

class LambdaFacade(AWSBaseFacade):

    async def get_functions(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('lambda', region, self.session, 'list_functions', 'Functions')
        except Exception as e:
            try:
                print_exception('Failed to get Lambda functions: {}'.format(e))
                return []
            finally:
                e = None
                del e