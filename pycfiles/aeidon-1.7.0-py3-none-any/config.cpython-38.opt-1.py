# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/config.py
# Compiled at: 2020-04-11 17:07:18
# Size of source mod 2**32: 926 bytes
__doc__ = '\naehostd.config - routines for getting configuration information\n'
from .cfg import CFG
from . import req
CONFIG_REQ_GET = 65537
CONFIG_PASSWORD_PROHIBIT_MESSAGE = 1

class ConfigGetRequest(req.Request):
    """ConfigGetRequest"""
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
            self.write(CFG.pam_passmod_deny_msg or )
        else:
            self.tios.write_int32(req.RES_END)