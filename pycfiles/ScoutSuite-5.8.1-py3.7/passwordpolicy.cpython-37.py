# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/iam/passwordpolicy.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1353 bytes
from ScoutSuite.providers.aws.resources.base import AWSResources

class PasswordPolicy(AWSResources):

    async def fetch_all(self):
        raw_password_policy = await self.facade.iam.get_password_policy()
        password_policy = self._parse_password_policy(raw_password_policy)
        self.update(password_policy)

    def _parse_password_policy(self, raw_password_policy):
        if raw_password_policy is None:
            return {'MinimumPasswordLength':'1',  'RequireUppercaseCharacters':False, 
             'RequireLowercaseCharacters':False, 
             'RequireNumbers':False, 
             'RequireSymbols':False, 
             'PasswordReusePrevention':False, 
             'ExpirePasswords':False}
        if 'PasswordReusePrevention' not in raw_password_policy:
            raw_password_policy['PasswordReusePrevention'] = False
        else:
            raw_password_policy['PreviousPasswordPrevented'] = raw_password_policy['PasswordReusePrevention']
            raw_password_policy['PasswordReusePrevention'] = True
        if 'MaxPasswordAge' in raw_password_policy:
            raw_password_policy['ExpirePasswords'] = True
        return raw_password_policy