# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/base/utils/auth.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 2164 bytes
import os
from arch.api.utils import file_utils

class FederationAuthorization(object):

    def __init__(self, transfer_conf_path):
        self.transfer_auth = {}
        for path, _, file_names in os.walk(os.path.join(file_utils.get_project_base_directory(), transfer_conf_path)):
            for name in file_names:
                transfer_conf = os.path.join(path, name)
                if transfer_conf.endswith('.json'):
                    self.transfer_auth.update(file_utils.load_json_conf(transfer_conf))

        self._authorized_src = {}
        self._authorized_dst = {}

    def _update_auth(self, variable_name):
        a_name, v_name = variable_name.split('.', 1)
        variable_auth = self.transfer_auth.get(a_name, {}).get(v_name, None)
        if variable_auth is None:
            raise ValueError(f"Unauthorized variable: {v_name}")
        auth_src = variable_auth['src']
        if not isinstance(auth_src, list):
            auth_src = [
             auth_src]
        auth_dst = variable_auth['dst']
        self._authorized_src[variable_name] = auth_src
        self._authorized_dst[variable_name] = auth_dst

    def authorized_src_roles(self, variable_name):
        if variable_name not in self._authorized_src:
            self._update_auth(variable_name)
        return self._authorized_src[variable_name]

    def authorized_dst_roles(self, variable_name):
        if variable_name not in self._authorized_dst:
            self._update_auth(variable_name)
        return self._authorized_dst[variable_name]