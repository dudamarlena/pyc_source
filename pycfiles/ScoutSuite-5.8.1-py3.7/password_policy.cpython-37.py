# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aliyun/resources/ram/password_policy.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1712 bytes
from ScoutSuite.providers.aliyun.resources.base import AliyunResources
from ScoutSuite.providers.aliyun.facade.base import AliyunFacade

class PasswordPolicy(AliyunResources):

    def __init__(self, facade):
        super(PasswordPolicy, self).__init__(facade)

    async def fetch_all(self):
        raw_password_policy = await self.facade.ram.get_password_policy()
        password_policy = self._parse_password_policy(raw_password_policy)
        self.update(password_policy)

    def _parse_password_policy(self, raw_password_policy):
        password_policy_dict = {'minimum_password_length':raw_password_policy.get('MinimumPasswordLength'), 
         'hard_expiry':raw_password_policy.get('HardExpiry'), 
         'max_login_attempts':raw_password_policy.get('MaxLoginAttemps'), 
         'max_password_age':raw_password_policy.get('MaxPasswordAge'), 
         'password_reuse_prevention':raw_password_policy.get('PasswordReusePrevention'), 
         'require_uppercase_characters':raw_password_policy.get('RequireUppercaseCharacters'), 
         'require_lowercase_characters':raw_password_policy.get('RequireLowercaseCharacters'), 
         'require_numbers':raw_password_policy.get('RequireNumbers'), 
         'require_symbols':raw_password_policy.get('RequireSymbols')}
        if password_policy_dict['password_reuse_prevention'] == 0:
            password_policy_dict['password_reuse_prevention'] = False
        else:
            password_policy_dict['password_reuse_prevention'] = True
            password_policy_dict['password_reuse_count'] = raw_password_policy.get('PasswordReusePrevention')
        return password_policy_dict