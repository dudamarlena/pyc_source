# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/apis/user_api.py
# Compiled at: 2018-03-12 09:48:15
# Size of source mod 2**32: 372 bytes
__doc__ = 'UserApi module class'
from ..common.base import Base

class UserApi(Base):

    def get_current_user(self):
        api_url = self._UserApi__get_api_url(model_name='me')
        return self.api_get(api_url)

    def __get_api_url(self, model_name='user', api_specifics=''):
        return self.get_api_url(model_name, api_specifics)