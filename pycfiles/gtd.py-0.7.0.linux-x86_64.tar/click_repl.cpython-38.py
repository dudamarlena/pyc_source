# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/delucks/.pyenv/versions/3.8.1/lib/python3.8/site-packages/todo/click_repl.py
# Compiled at: 2019-12-22 12:59:22
# Size of source mod 2**32: 7603 bytes
from collections import defaultdict
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import prompt
import click, click._bashcomplete, click.parser, os, shlex, sys, six
from todo.exceptions import GTDException
_internal_commands = dict()

def _register_internal_command(names, target, description=None):
    if not hasattr(target, '__call__'):
        raise ValueError('Internal command must be a callable')
    elif isinstance(names, six.string_types):
        names = [
         names]
    else:
        if not isinstance(names, (list, tuple)):
            raise ValueError('"names" must be a string or a list / tuple')
    for name in names:
        _internal_commands[name] = (
         target, description)


def _get_registered_target(name, default=None):
    target_info = _internal_commands.get(name)
    if target_info:
        return target_info[0]
    return default


def _exit_internal():
    raise GTDException()


def _help_internal():
    formatter = click.HelpFormatter()
    formatter.write_heading('REPL help')
    formatter.indent()
    with formatter.section('External Commands'):
        formatter.write_text('prefix external commands with "!"')
    with formatter.section('Internal Commands'):
        formatter.write_text('prefix internal commands with ":"')
        info_table = defaultdict(list)
        for mnemonic, target_info in six.iteritems(_internal_commands):
            info_table[target_info[1]].append(mnemonic)
        else:
            formatter.write_dl(((
             ', '.join((':{0}'.format(mnemonic) for mnemonic in sorted(mnemonics))), description) for description, mnemonics in six.iteritems(info_table)))

    return formatter.getvalue()


_register_internal_command(['q', 'quit', 'exit'], _exit_internal, 'exits the repl')
_register_internal_command(['?', 'h', 'help'], _help_internal, 'displays general help information')

class ClickCompleter(Completer):

    def __init__(self, cli):
        self.cli = cli

    def get_completions(self, document, complete_event=None):
        try:
            args = shlex.split(document.text_before_cursor)
        except ValueError:
            return
        else:
            cursor_within_command = document.text_before_cursor.rstrip() == document.text_before_cursor
            if args and cursor_within_command:
                incomplete = args.pop()
            else:
                incomplete = ''
            ctx = click._bashcomplete.resolve_ctx(self.cli, '', args)
            if ctx is None:
                return
            choices = []
            for param in ctx.command.params:
                if isinstance(param, click.Option):
                    for options in (
                     param.opts, param.secondary_opts):
                        for o in options:
                            choices.append(Completion(o, (-len(incomplete)), display_meta=(param.help)))

                elif isinstance(param, click.Argument) and isinstance(param.type, click.Choice):
                    for choice in param.type.choices:
                        choices.append(Completion(choice, -len(incomplete)))

            else:
                if isinstance(ctx.command, click.MultiCommand):
                    for name in ctx.command.list_commands(ctx):
                        command = ctx.command.get_command(ctx, name)
                        choices.append(Completion(name, (-len(incomplete)), display_meta=(getattr(command, 'short_help'))))

                for item in choices:
                    if item.text.startswith(incomplete):
                        (yield item)


def bootstrap_prompt(prompt_kwargs, group):
    """
    Bootstrap prompt_toolkit kwargs or use user defined values.

    :param prompt_kwargs: The user specified prompt kwargs.
    """
    prompt_kwargs = prompt_kwargs or {}
    defaults = {'history':InMemoryHistory(), 
     'completer':ClickCompleter(group),  'message':'> '}
    for key in defaults:
        default_value = defaults[key]
        if key not in prompt_kwargs:
            prompt_kwargs[key] = default_value
        return prompt_kwargs


def repl--- This code section failed: ---

 L. 150         0  LOAD_FAST                'old_ctx'
                2  LOAD_ATTR                parent
                4  JUMP_IF_TRUE_OR_POP     8  'to 8'
                6  LOAD_FAST                'old_ctx'
              8_0  COME_FROM             4  '4'
                8  STORE_FAST               'group_ctx'

 L. 151        10  LOAD_FAST                'group_ctx'
               12  LOAD_ATTR                command
               14  STORE_FAST               'group'

 L. 152        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                stdin
               20  LOAD_METHOD              isatty
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'isatty'

 L. 157        26  LOAD_FAST                'old_ctx'
               28  LOAD_ATTR                command
               30  LOAD_ATTR                name
               32  STORE_FAST               'repl_command_name'

 L. 158        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'group_ctx'
               38  LOAD_ATTR                command
               40  LOAD_GLOBAL              click
               42  LOAD_ATTR                CommandCollection
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_FALSE    68  'to 68'

 L. 159        48  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               50  LOAD_STR                 'repl.<locals>.<dictcomp>'
               52  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 160        54  LOAD_FAST                'group_ctx'
               56  LOAD_ATTR                command
               58  LOAD_ATTR                sources

 L. 159        60  GET_ITER         
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'available_commands'
               66  JUMP_FORWARD         76  'to 76'
             68_0  COME_FROM            46  '46'

 L. 163        68  LOAD_FAST                'group_ctx'
               70  LOAD_ATTR                command
               72  LOAD_ATTR                commands
               74  STORE_FAST               'available_commands'
             76_0  COME_FROM            66  '66'

 L. 164        76  LOAD_FAST                'available_commands'
               78  LOAD_METHOD              pop
               80  LOAD_FAST                'repl_command_name'
               82  LOAD_CONST               None
               84  CALL_METHOD_2         2  ''
               86  POP_TOP          

 L. 166        88  LOAD_GLOBAL              bootstrap_prompt
               90  LOAD_DEREF               'prompt_kwargs'
               92  LOAD_FAST                'group'
               94  CALL_FUNCTION_2       2  ''
               96  STORE_DEREF              'prompt_kwargs'

 L. 168        98  LOAD_FAST                'isatty'
              100  POP_JUMP_IF_FALSE   116  'to 116'

 L. 170       102  LOAD_CLOSURE             'prompt_kwargs'
              104  BUILD_TUPLE_1         1 
              106  LOAD_CODE                <code_object get_command>
              108  LOAD_STR                 'repl.<locals>.get_command'
              110  MAKE_FUNCTION_8          'closure'
              112  STORE_FAST               'get_command'
              114  JUMP_FORWARD        124  'to 124'
            116_0  COME_FROM           100  '100'

 L. 174       116  LOAD_GLOBAL              sys
              118  LOAD_ATTR                stdin
              120  LOAD_ATTR                readline
              122  STORE_FAST               'get_command'
            124_0  COME_FROM           114  '114'

 L. 177       124  SETUP_FINALLY       136  'to 136'

 L. 178       126  LOAD_FAST                'get_command'
              128  CALL_FUNCTION_0       0  ''
              130  STORE_FAST               'command'
              132  POP_BLOCK        
              134  JUMP_FORWARD        184  'to 184'
            136_0  COME_FROM_FINALLY   124  '124'

 L. 179       136  DUP_TOP          
              138  LOAD_GLOBAL              KeyboardInterrupt
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   158  'to 158'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 180       150  POP_EXCEPT       
              152  JUMP_BACK           124  'to 124'
              154  POP_EXCEPT       
              156  JUMP_FORWARD        184  'to 184'
            158_0  COME_FROM           142  '142'

 L. 181       158  DUP_TOP          
              160  LOAD_GLOBAL              EOFError
              162  COMPARE_OP               exception-match
              164  POP_JUMP_IF_FALSE   182  'to 182'
              166  POP_TOP          
              168  POP_TOP          
              170  POP_TOP          

 L. 182       172  POP_EXCEPT       
          174_176  BREAK_LOOP          478  'to 478'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
            182_0  COME_FROM           164  '164'
              182  END_FINALLY      
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           156  '156'
            184_2  COME_FROM           134  '134'

 L. 184       184  LOAD_FAST                'command'
              186  POP_JUMP_IF_TRUE    200  'to 200'

 L. 185       188  LOAD_FAST                'isatty'
              190  POP_JUMP_IF_FALSE   196  'to 196'

 L. 186       192  JUMP_BACK           124  'to 124'
              194  JUMP_FORWARD        200  'to 200'
            196_0  COME_FROM           190  '190'

 L. 188   196_198  BREAK_LOOP          478  'to 478'
            200_0  COME_FROM           194  '194'
            200_1  COME_FROM           186  '186'

 L. 190       200  LOAD_FAST                'allow_internal_commands'
          202_204  POP_JUMP_IF_FALSE   274  'to 274'

 L. 191       206  SETUP_FINALLY       246  'to 246'

 L. 192       208  LOAD_GLOBAL              handle_internal_commands
              210  LOAD_FAST                'command'
              212  CALL_FUNCTION_1       1  ''
              214  STORE_FAST               'result'

 L. 193       216  LOAD_GLOBAL              isinstance
              218  LOAD_FAST                'result'
              220  LOAD_GLOBAL              six
              222  LOAD_ATTR                string_types
              224  CALL_FUNCTION_2       2  ''
              226  POP_JUMP_IF_FALSE   242  'to 242'

 L. 194       228  LOAD_GLOBAL              click
              230  LOAD_METHOD              echo
              232  LOAD_FAST                'result'
              234  CALL_METHOD_1         1  ''
              236  POP_TOP          

 L. 195       238  POP_BLOCK        
              240  JUMP_BACK           124  'to 124'
            242_0  COME_FROM           226  '226'
              242  POP_BLOCK        
              244  JUMP_FORWARD        274  'to 274'
            246_0  COME_FROM_FINALLY   206  '206'

 L. 196       246  DUP_TOP          
              248  LOAD_GLOBAL              GTDException
              250  COMPARE_OP               exception-match
          252_254  POP_JUMP_IF_FALSE   272  'to 272'
              256  POP_TOP          
              258  POP_TOP          
              260  POP_TOP          

 L. 197       262  POP_EXCEPT       
          264_266  BREAK_LOOP          478  'to 478'
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
            272_0  COME_FROM           252  '252'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           244  '244'
            274_2  COME_FROM           202  '202'

 L. 199       274  SETUP_FINALLY       290  'to 290'

 L. 200       276  LOAD_GLOBAL              shlex
              278  LOAD_METHOD              split
              280  LOAD_FAST                'command'
              282  CALL_METHOD_1         1  ''
              284  STORE_FAST               'args'
              286  POP_BLOCK        
              288  JUMP_FORWARD        358  'to 358'
            290_0  COME_FROM_FINALLY   274  '274'

 L. 201       290  DUP_TOP          
              292  LOAD_GLOBAL              ValueError
              294  COMPARE_OP               exception-match
          296_298  POP_JUMP_IF_FALSE   356  'to 356'
              300  POP_TOP          
              302  STORE_FAST               'e'
              304  POP_TOP          
              306  SETUP_FINALLY       344  'to 344'

 L. 202       308  LOAD_GLOBAL              click
              310  LOAD_METHOD              echo
              312  LOAD_STR                 '{}: {}'
              314  LOAD_METHOD              format
              316  LOAD_GLOBAL              type
              318  LOAD_FAST                'e'
              320  CALL_FUNCTION_1       1  ''
              322  LOAD_ATTR                __name__
              324  LOAD_FAST                'e'
              326  CALL_METHOD_2         2  ''
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          

 L. 203       332  POP_BLOCK        
              334  POP_EXCEPT       
              336  CALL_FINALLY        344  'to 344'
              338  JUMP_BACK           124  'to 124'
              340  POP_BLOCK        
              342  BEGIN_FINALLY    
            344_0  COME_FROM           336  '336'
            344_1  COME_FROM_FINALLY   306  '306'
              344  LOAD_CONST               None
              346  STORE_FAST               'e'
              348  DELETE_FAST              'e'
              350  END_FINALLY      
              352  POP_EXCEPT       
              354  JUMP_FORWARD        358  'to 358'
            356_0  COME_FROM           296  '296'
              356  END_FINALLY      
            358_0  COME_FROM           354  '354'
            358_1  COME_FROM           288  '288'

 L. 205       358  SETUP_FINALLY       410  'to 410'

 L. 206       360  LOAD_FAST                'group'
              362  LOAD_ATTR                make_context
              364  LOAD_CONST               None
              366  LOAD_FAST                'args'
              368  LOAD_FAST                'group_ctx'
              370  LOAD_CONST               ('parent',)
              372  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              374  SETUP_WITH          400  'to 400'
              376  STORE_FAST               'ctx'

 L. 207       378  LOAD_FAST                'group'
              380  LOAD_METHOD              invoke
              382  LOAD_FAST                'ctx'
              384  CALL_METHOD_1         1  ''
              386  POP_TOP          

 L. 208       388  LOAD_FAST                'ctx'
              390  LOAD_METHOD              exit
              392  CALL_METHOD_0         0  ''
              394  POP_TOP          
              396  POP_BLOCK        
              398  BEGIN_FINALLY    
            400_0  COME_FROM_WITH      374  '374'
              400  WITH_CLEANUP_START
              402  WITH_CLEANUP_FINISH
              404  END_FINALLY      
              406  POP_BLOCK        
              408  JUMP_BACK           124  'to 124'
            410_0  COME_FROM_FINALLY   358  '358'

 L. 209       410  DUP_TOP          
              412  LOAD_GLOBAL              click
              414  LOAD_ATTR                ClickException
              416  COMPARE_OP               exception-match
          418_420  POP_JUMP_IF_FALSE   454  'to 454'
              422  POP_TOP          
              424  STORE_FAST               'e'
              426  POP_TOP          
              428  SETUP_FINALLY       442  'to 442'

 L. 210       430  LOAD_FAST                'e'
              432  LOAD_METHOD              show
              434  CALL_METHOD_0         0  ''
              436  POP_TOP          
              438  POP_BLOCK        
              440  BEGIN_FINALLY    
            442_0  COME_FROM_FINALLY   428  '428'
              442  LOAD_CONST               None
              444  STORE_FAST               'e'
              446  DELETE_FAST              'e'
              448  END_FINALLY      
              450  POP_EXCEPT       
              452  JUMP_BACK           124  'to 124'
            454_0  COME_FROM           418  '418'

 L. 211       454  DUP_TOP          
              456  LOAD_GLOBAL              SystemExit
              458  COMPARE_OP               exception-match
          460_462  POP_JUMP_IF_FALSE   474  'to 474'
              464  POP_TOP          
              466  POP_TOP          
              468  POP_TOP          

 L. 212       470  POP_EXCEPT       
              472  JUMP_BACK           124  'to 124'
            474_0  COME_FROM           460  '460'
              474  END_FINALLY      
              476  JUMP_BACK           124  'to 124'

Parse error at or near `POP_EXCEPT' instruction at offset 154


def register_repl(group, name='repl'):
    """Register :func:`repl()` as sub-command *name* of *group*."""
    group.command(name=name)(click.pass_context(repl))


def handle_internal_commands(command):
    """Run repl-internal commands.

    Repl-internal commands are all commands starting with ":".

    """
    if command.startswith(':'):
        target = _get_registered_target((command[1:]), default=None)
        if target:
            return target()