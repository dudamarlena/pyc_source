# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/powercmd/cmd.py
# Compiled at: 2020-03-22 15:23:25
# Size of source mod 2**32: 6863 bytes
"""
powercmd - A generic class to build typesafe line-oriented command interpreters.

As in Cmd module, methods starting with 'do_' are considered command handlers.
That behavior can be changed by overriding the `get_command_prefixes` method.

All command handler arguments must have a type annotation. Actual values passed
to the command handler are not strings typed by the user, but objects of
appropriate types hinted by the annotations, which are constructed as follows:

1. If the type hinted by an annotation contains a static `powercmd_parse`
   function, it is called with a single string argument. The return value of
   `powercmd_parse` is passed to the command handler and is expected to be an
   instance of the annotated type.
2. Otherwise, the value is created by calling the constructor of the annotated
   type with a single argument: a string typed by the user.

Example:
    class SimpleTestCmd(powercmd.Cmd):
        def do_test_command(self,
                            int_arg: int):
            # `test_command 123` translates to `do_test_command(int('123'))`
            pass

        class CustomType:
            @staticmethod
            def powercmd_parse(text):
                return CustomType()

        def do_test_custom(self,
                           custom_arg: CustomType):
            # `test_custom 123` translates to
            # `do_test_custom(CustomType.powercmd_parse('123'))`
            pass
"""
import inspect, os, sys, traceback
from prompt_toolkit import PromptSession
from prompt_toolkit.history import History
import prompt_toolkit.patch_stdout as patch_stdout
from prompt_toolkit.styles import Style
from powercmd.command import Command
from powercmd.command_invoker import CommandInvoker
from powercmd.command_line import CommandLine
from powercmd.commands_dict import CommandsDict
from powercmd.completer import Completer
from powercmd.exceptions import InvalidInput

class Cmd:
    __doc__ = '\n    A simple framework for writing typesafe line-oriented command interpreters.\n    '

    def __init__(self, history: History=None):
        self._last_exception = None
        self._session = PromptSession(history=history)
        self.prompt = '> '
        self.prompt_style = Style.from_dict({'': 'bold'})

    def get_command_prefixes(self):
        """
        Returns a mapping {method_command_prefix -> input_string_prefix}.
        input_string_prefix is a prefix of a command typed in the command line,
        method_command_prefix is the prefix for a matching command.

        If this function returns {'do_': ''}, then all methods whose names start
        with 'do_' will be available as commands with the same names, i.e.
        typing 'foo' will execute 'do_foo'.
        If it returned {'do_',\xa0'!'}, then one has to type '!foo' in order to
        execute 'do_foo'.
        """
        return {'do_': ''}

    def do_get_error(self):
        """
        Displays an exception thrown by last command.
        """
        if self._last_exception is None:
            print('no errors')
        else:
            (traceback.print_exception)(*self._last_exception)

    def do_exit(self):
        """Terminates the command loop."""
        print('exiting')
        return True

    def do_EOF(self):
        """Terminates the command loop."""
        print('')
        return self.do_exit()

    def do_help(self, topic: str=''):
        """
        Displays a description of given command or lists all available commands.
        """
        cmds = self._get_all_commands()
        if not topic:
            print('available commands: %s' % (' '.join(sorted(cmds)),))
            return
        try:
            handler = cmds.choose(topic, verbose=True)
            print(handler.help)
        except InvalidInput:
            print('no such command: %s' % (topic,))
            print('available commands: %s' % (' '.join(sorted(cmds)),))

    def _get_all_commands(self) -> CommandsDict:
        """Returns all defined commands."""
        import types

        def unbind(f):
            if not callable(f):
                raise TypeError('%s is not callable' % (repr(f),))
            else:
                self = getattr(f, '__self__', None)
                if self is not None:
                    if not isinstance(self, types.ModuleType):
                        if not isinstance(self, type):
                            if hasattr(f, '__func__'):
                                return f.__func__
                            return getattr(type(f.__self__), f.__name__)
            return f

        members = inspect.getmembers(self)
        prefixes = self.get_command_prefixes()
        commands = CommandsDict()
        for name, handler in members:
            if not callable(handler):
                continue
            for prefix, substitution in prefixes.items():
                if name.startswith(prefix):
                    assert substitution + name not in commands
                    cmd_name = substitution + name[len(prefix):]
                    commands[cmd_name] = Command(name=cmd_name, handler=(unbind(handler)))

        return commands

    def emptyline(self):
        """
        Method called whenever the user enters an empty line.
        """
        pass

    def default--- This code section failed: ---

 L. 167         0  SETUP_EXCEPT         44  'to 44'

 L. 168         2  LOAD_FAST                'cmdline'
                4  POP_JUMP_IF_TRUE     14  'to 14'

 L. 169         6  LOAD_FAST                'self'
                8  LOAD_METHOD              emptyline
               10  CALL_METHOD_0         0  '0 positional arguments'
               12  RETURN_VALUE     
             14_0  COME_FROM             4  '4'

 L. 171        14  LOAD_GLOBAL              CommandInvoker
               16  LOAD_FAST                'self'
               18  LOAD_METHOD              _get_all_commands
               20  CALL_METHOD_0         0  '0 positional arguments'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  STORE_FAST               'invoker'

 L. 172        26  LOAD_FAST                'invoker'
               28  LOAD_ATTR                invoke
               30  LOAD_FAST                'self'
               32  LOAD_GLOBAL              CommandLine
               34  LOAD_FAST                'cmdline'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  LOAD_CONST               ('cmdline',)
               40  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               42  RETURN_VALUE     
             44_0  COME_FROM_EXCEPT      0  '0'

 L. 175        44  DUP_TOP          
               46  LOAD_GLOBAL              Exception
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    98  'to 98'
               52  POP_TOP          
               54  STORE_FAST               'e'
               56  POP_TOP          
               58  SETUP_FINALLY        86  'to 86'

 L. 176        60  LOAD_GLOBAL              sys
               62  LOAD_METHOD              exc_info
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _last_exception

 L. 177        70  LOAD_GLOBAL              print
               72  LOAD_STR                 '%s (try "get_error" for details)'
               74  LOAD_FAST                'e'
               76  BINARY_MODULO    
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  POP_TOP          
               82  POP_BLOCK        
               84  LOAD_CONST               None
             86_0  COME_FROM_FINALLY    58  '58'
               86  LOAD_CONST               None
               88  STORE_FAST               'e'
               90  DELETE_FAST              'e'
               92  END_FINALLY      
               94  POP_EXCEPT       
               96  JUMP_FORWARD        106  'to 106'
             98_0  COME_FROM            50  '50'
               98  END_FINALLY      

 L. 179       100  LOAD_CONST               None
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _last_exception
            106_0  COME_FROM            96  '96'

Parse error at or near `STORE_ATTR' instruction at offset 104

    def onecmd(self, cmdline):
        """
        Interprets CMDLINE as a command and executes it.
        """
        return self.default(cmdline)

    def cmdloop(self):
        """
        Interprets commands read from stdin until a shutdown is requested or
        EOF encountered.
        """
        completer = Completer(self._get_all_commands())
        try:
            while True:
                if os.isatty(sys.stdin.fileno()):
                    with patch_stdout():
                        cmd = self._session.prompt((self.prompt), completer=completer, style=(self.prompt_style))
                else:
                    cmd = input(self.prompt)
                self.onecmd(cmd)

        except EOFError:
            pass