# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/utils/schemas.py
# Compiled at: 2019-10-27 19:02:52
# Size of source mod 2**32: 577 bytes
from rest_framework.schemas import AutoSchema

class CustomSchema(AutoSchema):

    def _allows_filters(self, path, method):
        if method.lower() != 'get':
            return False
        if getattr(self.view, 'filter_backends', None) is None:
            return False
        if hasattr(self.view, 'action'):
            if self.view.action in ('retrieve', 'update', 'partial_update', 'destroy'):
                return False
            if self.view.action == 'list':
                return True
            return self.view.action[(-1)] == 's'
        return False