# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-MsePIp/scf/tcfcli/cmds/native/common/runtime.py
# Compiled at: 2019-12-02 05:04:19
from tcfcli.common.tcsam.tcsam_macro import TcSamMacro as tsmacro
from tcfcli.common.user_exceptions import InvalidTemplateException
from tcfcli.common.macro import MacroRuntime

class Runtime(object):
    RUNTIME = {MacroRuntime.node610: MacroRuntime.cmd_node610, 
       MacroRuntime.node89: MacroRuntime.cmd_node89, 
       MacroRuntime.node89_s: MacroRuntime.cmd_node89_s, 
       MacroRuntime.python36: MacroRuntime.cmd_python36, 
       MacroRuntime.python27: MacroRuntime.cmd_python27}

    def __init__(self, proper):
        self.codeuri = proper.get(tsmacro.CodeUri)
        self.env = proper.get(tsmacro.Envi, {tsmacro.Vari: {}}).get(tsmacro.Vari, {})
        self.handler = proper.get(tsmacro.Handler)
        self.mem_size = proper.get(tsmacro.MemSize)
        self.runtime = proper.get(tsmacro.Runtime, '').lower()
        self.timeout = proper.get(tsmacro.Timeout, 3)
        if self.runtime not in self.RUNTIME.keys():
            raise InvalidTemplateException(('Invalid runtime. supports [{}]').format((',').join(self.RUNTIME.keys())))

    @property
    def cmd(self):
        return self.RUNTIME[self.runtime]