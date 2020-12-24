# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grudin/dev/my/api-cloudvps-py/.venv/lib/python3.7/site-packages/cloudvps/objects/common.py
# Compiled at: 2018-10-01 13:52:32
# Size of source mod 2**32: 810 bytes
from .base import Cloud

class Common(Cloud):
    __doc__ = '\n    Common functions\n    '

    def __init__(self, api):
        super(Common, self).__init__(api)

    def sizes(self):
        """
        Get all plans
        """
        data = self.api.get('/sizes')
        return data

    def get_new_name(self):
        """
        Get random name
        """
        data = self.api.get('/random_reglet_name')
        return data

    def estimate(self):
        """
        Get average time of operation
        """
        data = self.api.get('/estimate')
        return data

    def validate(self, param_name, value):
        """
        Validate parameter ( param_name : value )
        """
        payload = {param_name: value}
        data = self.api.post('/validate', payload)
        return data