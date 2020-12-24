# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/casper/services/iam.py
# Compiled at: 2020-01-30 17:53:06
# Size of source mod 2**32: 734 bytes
from casper.services.base import BaseService

class IAMService(BaseService):

    def __init__(self, profile=None):
        super().__init__(profile=profile)
        self._resources_groups = ['aws_iam_user', 'aws_iam_role']

    def _get_live_aws_iam_user(self):
        iam_client = self.session.client('iam')
        iam_users = iam_client.list_users()
        users = {user['UserName']:user for user in iam_users['Users']}
        return users

    def _get_live_aws_iam_role(self):
        iam_client = self.session.client('iam')
        iam_roles = iam_client.list_roles()
        roles = {role['RoleName']:role for role in iam_roles['Roles']}
        return roles

    def scan_service(self, ghosts):
        pass