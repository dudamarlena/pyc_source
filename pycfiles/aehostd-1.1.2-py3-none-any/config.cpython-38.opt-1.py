# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aehostd/config.py
# Compiled at: 2020-04-11 17:07:18
# Size of source mod 2**32: 926 bytes
"""
aehostd.config - routines for getting configuration information
"""
from .cfg import CFG
from . import req
CONFIG_REQ_GET = 65537
CONFIG_PASSWORD_PROHIBIT_MESSAGE = 1

class ConfigGetRequest(req.Request):
    __doc__ = '\n    handle password change requests (mainly denying them)\n    '
    rtype = CONFIG_REQ_GET

    def _read_params(self) -> dict:
        return dict(cfgopt=(self.tios.read_int32()))

    def write(self, value):
        self.tios.write_int32(req.RES_BEGIN)
        self.tios.write_string(value)
        self.tios.write_int32(req.RES_END)

    def process(self):
        """
        reject the password change request
        """
        cfgopt = self._params['cfgopt']
        if cfgopt == CONFIG_PASSWORD_PROHIBIT_MESSAGE:
            self.write(CFG.pam_passmod_deny_msg or '')
        else:
            self.tios.write_int32(req.RES_END)