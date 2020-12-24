# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /botfly/controller.py
# Compiled at: 2019-11-10 21:14:18
# Size of source mod 2**32: 4728 bytes
"""
Controller component module.
"""
__all__ = [
 'CommandController']
import sys
from prompt_toolkit.completion import DummyCompleter
from . import commands
from . import exceptions
from . import docopt

class CommandController:
    __doc__ = 'Controller wraps a UI and object with commands.\n\n    Manageds completion scopes, calling methods on commands and dealing with\n    errors.\n\n    Provides built-in docopt support. The method\'s docstring is inspected for\n    *Usage:* section and arguments parsed, with the argument dictionary passed as\n    parameter to to command method.\n\n    With our without a *Usage* section, the arguments will have an "argv" key\n    referencing the original argv value from the parser.\n    '

    def __init__(self, commands):
        self.commands = commands
        self._completion_scopes = {}
        self._command_list = None
        self._ui = commands._ui
        self.environ = self._ui.environ

    def except_hook(self, ex, val, tb):
        self._ui.error('{}: {}'.format(ex.__name__, val))

    def handle_subcommand_exit(self, value):
        pass

    def finalize(self):
        self.commands.finalize()

    def add_completion_scope(self, name, completer):
        self._completion_scopes[name] = completer

    def get_completion_scope(self, name):
        return self._completion_scopes.get(name, DummyCompleter())

    def remove_completion_scope(self, name):
        del self._completion_scopes[name]

    def getarg(self, argv, index, default=None):
        if len(argv) > index:
            return argv[index]
        return default

    def call(self, argv):
        """Dispatch command method by calling with an argv that has the method
        name as first element.
        """
        if argv:
            if not argv[0] or argv[0].startswith('_'):
                return 2
            argv = self._expand_aliases(argv)
            if argv[0].startswith('#'):
                return 0
        else:
            meth = getattr(self.commands, argv[0], self.commands.default_command)
            try:
                arguments = docopt.docopt((meth.__doc__), argv=(argv[1:]),
                  help=False,
                  version=None,
                  options_first=True)
                arguments['argv'] = argv
            except docopt.DocoptLanguageError:
                arguments = {'argv': argv}
            except docopt.DocoptExit as docerr:
                try:
                    self._ui.warning(str(docerr))
                    return 2
                finally:
                    docerr = None
                    del docerr

        try:
            rv = meth(arguments)
        except (exceptions.NewCommand, exceptions.CommandQuit,
         exceptions.CommandExit,
         KeyboardInterrupt):
            raise
        except:
            ex, val, tb = sys.exc_info()
            self.except_hook(ex, val, tb)
        else:
            if rv is not None:
                try:
                    self._ui.environ['?'] = int(rv)
                except (ValueError, TypeError, AttributeError):
                    self._ui.environ['?'] = 0

                self._ui.environ['_'] = rv
            return rv

    def _expand_aliases(self, argv):
        seen = {}
        while 1:
            alias = self.commands._aliases.get(argv[0], None)
            if alias:
                if alias[0] in seen:
                    break
                seen[alias[0]] = True
                del argv[0]
                rl = alias[:]
                rl.reverse()
                for arg in rl:
                    argv.insert(0, arg)

            else:
                break

        return argv

    def get_command_names(self):
        if self._command_list is None:
            self._command_list = commands.get_command_list(self.commands)
        return self._command_list