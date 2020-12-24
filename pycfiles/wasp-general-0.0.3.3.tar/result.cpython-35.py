# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/command/result.py
# Compiled at: 2017-12-19 08:04:31
# Size of source mod 2**32: 2377 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from wasp_general.verify import verify_type
from wasp_general.command.proto import WCommandResultProto

class WCommandEnv(WCommandResultProto):

    def __init__(self, **command_env):
        WCommandResultProto.__init__(self)
        self._WCommandEnv__command_env = command_env

    def environment(self):
        return self._WCommandEnv__command_env.copy()


class WPlainCommandResult(WCommandEnv):

    @verify_type(result=str)
    def __init__(self, result, **command_env):
        WCommandEnv.__init__(self, **command_env)
        self._WPlainCommandResult__result = result

    def __str__(self):
        return self._WPlainCommandResult__result

    @classmethod
    def error(cls, message, **command_env):
        return WPlainCommandResult('Error. ' + message, **command_env)


class WExceptionResult(WCommandEnv):

    @verify_type(message=str, exception=Exception)
    def __init__(self, message, exc, traceback, **command_env):
        WCommandEnv.__init__(self, **command_env)
        self._WExceptionResult__message = message
        self._WExceptionResult__exception = str(exc)
        self._WExceptionResult__traceback = traceback

    def message(self):
        return self._WExceptionResult__message

    def exception(self):
        return self._WExceptionResult__exception

    def traceback(self):
        return self._WExceptionResult__traceback

    def __str__(self):
        return '%s\nException was raised. %s\n%s' % (
         self.message(), self.exception(), self.traceback())