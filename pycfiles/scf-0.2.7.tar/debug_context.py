# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-MsePIp/scf/tcfcli/cmds/native/common/debug_context.py
# Compiled at: 2019-12-02 05:04:19
from tcfcli.common.user_exceptions import InvalidOptionValue
from tcfcli.common.macro import MacroRuntime
from tcfcli.common.user_config import UserConfig

class DebugContext(object):
    DEBUG_CMD = {MacroRuntime.node610: MacroRuntime.cmd_node610, 
       MacroRuntime.node89: MacroRuntime.cmd_node89, 
       MacroRuntime.node89_s: MacroRuntime.cmd_node89_s, 
       MacroRuntime.python27: MacroRuntime.cmd_python27, 
       MacroRuntime.python36: MacroRuntime.cmd_python36}

    def __init__(self, port, argv, runtime):
        self.debug_port = port
        self.debug_argv = argv
        self.runtime = runtime

    @property
    def is_debug(self):
        return self.debug_port is not None

    @property
    def cmd(self):
        if self.debug_port is None:
            if self.runtime == 'python3.6' and UserConfig().python3_path.upper() != 'NONE':
                return UserConfig().python3_path
            else:
                if self.runtime == 'python2.7' and UserConfig().python2_path.upper() != 'NONE':
                    return UserConfig().python2_path
                return self.DEBUG_CMD[self.runtime]

        return

    @property
    def argv(self):
        if self.debug_port is None:
            return []
        else:
            argv = []
            if self.debug_argv:
                argv.append(self.debug_argv)
            if self.runtime not in self.DEBUG_CMD.keys():
                raise InvalidOptionValue(('Invalid runtime. [{}] support debug').format((',').join(self.DEBUG_CMD.keys())))
            if self.runtime == MacroRuntime.node610:
                argv += self.debug_arg_node610
            elif self.runtime == MacroRuntime.node89:
                argv += self.debug_arg_node89
            elif self.runtime == MacroRuntime.node89_s:
                argv += self.debug_arg_node89
            elif self.runtime == MacroRuntime.python36:
                argv += self.debug_arg_python36
            elif self.runtime == MacroRuntime.python27:
                argv += self.debug_arg_python27
            return argv

    @property
    def debug_arg_node610(self):
        return [
         '--inspect',
         '--debug-brk=' + str(self.debug_port),
         '--nolazy',
         '--max-old-space-size=2547',
         '--max-semi-space-size=150',
         '--expose-gc']

    @property
    def debug_arg_node89(self):
        return [
         '--inspect-brk=0.0.0.0:' + str(self.debug_port),
         '--nolazy',
         '--expose-gc',
         '--max-semi-space-size=150',
         '--max-old-space-size=2707']

    @property
    def debug_arg_python36(self):
        return [
         '-m',
         'ptvsd',
         '--host',
         '0.0.0.0',
         '--port',
         str(self.debug_port),
         '--wait']

    @property
    def debug_arg_python27(self):
        return [
         '-m',
         'ptvsd',
         '--host',
         '0.0.0.0',
         '--port',
         str(self.debug_port),
         '--wait']