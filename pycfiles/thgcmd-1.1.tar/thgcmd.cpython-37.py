# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/thgcmd.py
# Compiled at: 2019-07-17 15:13:03
# Size of source mod 2**32: 193686 bytes
"""Variant on standard library's cmd with extra features.

To use, simply import thgcmd.Cmd instead of cmd.Cmd; use precisely as though you
were using the standard library's cmd, while enjoying the extra features.

Searchable command history (commands: "history")
Run commands from file, save to file, edit commands in file
Multi-line commands
Special-character shortcut commands (beyond cmd's "?" and "!")
Settable environment parameters
Parsing commands with `argparse` argument parsers (flags)
Redirection to file or paste buffer (clipboard) with > or >>
Easy transcript-based testing of applications (see examples/example.py)
Bash-style ``select`` available

Note that redirection with > and | will only work if `self.poutput()`
is used in place of `print`.

- Catherine Devlin, Jan 03 2008 - catherinedevlin.blogspot.com

Git repository on GitHub at https://github.com/python-cmd2/cmd2
"""
import argparse, cmd, glob, inspect, os, pickle, re, sys, threading
from collections import namedtuple
from contextlib import redirect_stdout
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Tuple, Type, Union
from . import ArgParser, CompletionItem
from . import ansi
from . import constants
from . import plugin
from . import utils
from .clipboard import can_clip, get_paste_buffer, write_to_paste_buffer
from .history import History, HistoryItem
from .parsing import StatementParser, Statement, Macro, MacroArg, shlex_split
from .rl_utils import rl_type, RlType, rl_get_point, rl_set_prompt, vt100_support, rl_make_safe_prompt
if rl_type == RlType.NONE:
    rl_warning = 'Readline features including tab completion have been disabled since no \nsupported version of readline was found. To resolve this, install \npyreadline on Windows or gnureadline on Mac.\n\n'
    sys.stderr.write(ansi.style_warning(rl_warning))
else:
    from .rl_utils import rl_force_redisplay, readline
    orig_rl_delims = readline.get_completer_delims()
    if rl_type == RlType.PYREADLINE:
        orig_pyreadline_display = readline.rl.mode._display_completions
    else:
        if rl_type == RlType.GNU:
            import ctypes
            from .rl_utils import readline_lib
            rl_basic_quote_characters = ctypes.c_char_p.in_dll(readline_lib, 'rl_basic_quote_characters')
            orig_rl_basic_quotes = ctypes.cast(rl_basic_quote_characters, ctypes.c_void_p).value
        ipython_available = True
        try:
            from IPython import embed
        except ImportError:
            ipython_available = False

        HELP_CATEGORY = 'help_category'
        INTERNAL_COMMAND_EPILOG = 'Notes:\n  This command is for internal use and is not intended to be called from the\n  command line.'
        COMMAND_FUNC_PREFIX = 'thgcmd_'
        HELP_FUNC_PREFIX = 'help_'
        ALPHABETICAL_SORT_KEY = utils.norm_fold
        NATURAL_SORT_KEY = utils.natural_keys
        COMMAND_NAME = '<COMMAND_NAME>'

        def categorize(func: Union[(Callable, Iterable)], category: str) -> None:
            """Categorize a function.

    The help command output will group this function under the specified category heading

    :param func: function to categorize
    :param category: category to put it in
    """
            if isinstance(func, Iterable):
                for item in func:
                    setattr(item, HELP_CATEGORY, category)

            else:
                setattr(func, HELP_CATEGORY, category)


        def with_category(category: str) -> Callable:
            """A decorator to apply a category to a command function."""

            def cat_decorator(func):
                categorize(func, category)
                return func

            return cat_decorator


        def with_argument_list(*args: List[Callable], preserve_quotes: bool=False) -> Callable[([List], Optional[bool])]:
            """A decorator to alter the arguments passed to a thgcmd_* thgcmd method. Default passes a string of whatever the user
    typed. With this decorator, the decorated method will receive a list of arguments parsed from user input.

    :param args: Single-element positional argument list containing thgcmd_* method this decorator is wrapping
    :param preserve_quotes: if True, then argument quotes will not be stripped
    :return: function that gets passed a list of argument strings
    """
            import functools

            def arg_decorator(func):

                @functools.wraps(func)
                def cmd_wrapper(cmd2_instance, statement):
                    _, parsed_arglist = cmd2_instance.statement_parser.get_command_arg_list(command_name, statement, preserve_quotes)
                    return func(cmd2_instance, parsed_arglist)

                command_name = func.__name__[len(COMMAND_FUNC_PREFIX):]
                cmd_wrapper.__doc__ = func.__doc__
                return cmd_wrapper

            if len(args) == 1:
                if callable(args[0]):
                    return arg_decorator(args[0])
            return arg_decorator


        def with_argparser_and_unknown_args(argparser: argparse.ArgumentParser, *, ns_provider: Optional[Callable[(..., argparse.Namespace)]]=None, preserve_quotes: bool=False) -> Callable[([argparse.Namespace, List], Optional[bool])]:
            """A decorator to alter a thgcmd method to populate its ``args`` argument by parsing arguments with the given
    instance of argparse.ArgumentParser, but also returning unknown args as a list.

    :param argparser: unique instance of ArgumentParser
    :param ns_provider: An optional function that accepts a thgcmd.Cmd object as an argument and returns an
                        argparse.Namespace. This is useful if the Namespace needs to be prepopulated with
                        state data that affects parsing.
    :param preserve_quotes: if True, then arguments passed to argparse maintain their quotes
    :return: function that gets passed argparse-parsed args in a Namespace and a list of unknown argument strings
             A member called __statement__ is added to the Namespace to provide command functions access to the
             Statement object. This can be useful if the command function needs to know the command line.

    """
            import functools

            def arg_decorator(func):

                @functools.wraps(func)
                def cmd_wrapper(cmd2_instance, statement):
                    statement, parsed_arglist = cmd2_instance.statement_parser.get_command_arg_list(command_name, statement, preserve_quotes)
                    if ns_provider is None:
                        namespace = None
                    else:
                        namespace = ns_provider(cmd2_instance)
                    try:
                        args, unknown = argparser.parse_known_args(parsed_arglist, namespace)
                    except SystemExit:
                        return
                    else:
                        setattr(args, '__statement__', statement)
                        return func(cmd2_instance, args, unknown)

                command_name = func.__name__[len(COMMAND_FUNC_PREFIX):]
                argparser.prog = command_name
                if argparser.description is None:
                    if func.__doc__:
                        argparser.description = func.__doc__
                cmd_wrapper.__doc__ = argparser.description
                setattr(cmd_wrapper, 'argparser', argparser)
                return cmd_wrapper

            return arg_decorator


        def with_argparser(argparser: argparse.ArgumentParser, *, ns_provider: Optional[Callable[(..., argparse.Namespace)]]=None, preserve_quotes: bool=False) -> Callable[([argparse.Namespace], Optional[bool])]:
            """A decorator to alter a thgcmd method to populate its ``args`` argument by parsing arguments
    with the given instance of argparse.ArgumentParser.

    :param argparser: unique instance of ArgumentParser
    :param ns_provider: An optional function that accepts a thgcmd.Cmd object as an argument and returns an
                        argparse.Namespace. This is useful if the Namespace needs to be prepopulated with
                        state data that affects parsing.
    :param preserve_quotes: if True, then arguments passed to argparse maintain their quotes
    :return: function that gets passed the argparse-parsed args in a Namespace
             A member called __statement__ is added to the Namespace to provide command functions access to the
             Statement object. This can be useful if the command function needs to know the command line.
    """
            import functools

            def arg_decorator(func):

                @functools.wraps(func)
                def cmd_wrapper(cmd2_instance, statement):
                    statement, parsed_arglist = cmd2_instance.statement_parser.get_command_arg_list(command_name, statement, preserve_quotes)
                    if ns_provider is None:
                        namespace = None
                    else:
                        namespace = ns_provider(cmd2_instance)
                    try:
                        args = argparser.parse_args(parsed_arglist, namespace)
                    except SystemExit:
                        return
                    else:
                        setattr(args, '__statement__', statement)
                        return func(cmd2_instance, args)

                command_name = func.__name__[len(COMMAND_FUNC_PREFIX):]
                argparser.prog = command_name
                if argparser.description is None:
                    if func.__doc__:
                        argparser.description = func.__doc__
                cmd_wrapper.__doc__ = argparser.description
                setattr(cmd_wrapper, 'argparser', argparser)
                return cmd_wrapper

            return arg_decorator


        class EmbeddedConsoleExit(SystemExit):
            __doc__ = 'Custom exception class for use with the py command.'


        class EmptyStatement(Exception):
            __doc__ = 'Custom exception class for handling behavior when the user just presses <Enter>.'


        DisabledCommand = namedtuple('DisabledCommand', ['command_function', 'help_function'])

        class Cmd(cmd.Cmd):
            __doc__ = 'An easy but powerful framework for writing line-oriented command interpreters.\n\n    Extends the Python Standard Library’s cmd package by adding a lot of useful features\n    to the out of the box configuration.\n\n    Line-oriented command interpreters are often useful for test harnesses, internal tools, and rapid prototypes.\n    '
            DEFAULT_EDITOR = utils.find_editor()

            def __init__(self, completekey='tab', stdin=None, stdout=None, *, persistent_history_file='', persistent_history_length=1000, startup_script=None, use_ipython=False, allow_cli_args=True, transcript_files=None, allow_redirection=True, multiline_commands=None, terminators=None, shortcuts=None):
                """An easy but powerful framework for writing line-oriented command interpreters, extends Python's cmd package.

        :param completekey: readline name of a completion key, default to Tab
        :param stdin: alternate input file object, if not specified, sys.stdin is used
        :param stdout: alternate output file object, if not specified, sys.stdout is used
        :param persistent_history_file: file path to load a persistent thgcmd command history from
        :param persistent_history_length: max number of history items to write to the persistent history file
        :param startup_script: file path to a script to execute at startup
        :param use_ipython: should the "ipy" command be included for an embedded IPython shell
        :param allow_cli_args: if True, then thgcmd will process command line arguments as either
                               commands to be run or, if -t is specified, transcript files to run.
                               This should be set to False if your application parses its own arguments.
        :param transcript_files: allow running transcript tests when allow_cli_args is False
        :param allow_redirection: should output redirection and pipes be allowed
        :param multiline_commands: list of commands allowed to accept multi-line input
        :param shortcuts: dictionary containing shortcuts for commands
        """
                if not use_ipython:
                    try:
                        del Cmd.thgcmd_ipy
                    except AttributeError:
                        pass

                    self._initialize_plugin_system()
                    super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
                    self.default_to_shell = False
                    self.quit_on_sigint = False
                    self.continuation_prompt = '> '
                    self.debug = False
                    self.echo = False
                    self.editor = self.DEFAULT_EDITOR
                    self.feedback_to_output = False
                    self.locals_in_py = False
                    self.max_completion_items = 50
                    self.quiet = False
                    self.timing = False
                    self.settable = {'allow_ansi':'Allow ANSI escape sequences in output (valid values: {}, {}, {})'.format(ansi.ANSI_TERMINAL, ansi.ANSI_ALWAYS, ansi.ANSI_NEVER), 
                     'continuation_prompt':'On 2nd+ line of input', 
                     'debug':'Show full error stack on error', 
                     'echo':'Echo command issued into output', 
                     'editor':'Program used by ``edit``', 
                     'feedback_to_output':'Include nonessentials in `|`, `>` results', 
                     'locals_in_py':'Allow access to your application in py via self', 
                     'max_completion_items':'Maximum number of CompletionItems to display during tab completion', 
                     'prompt':'The prompt issued to solicit input', 
                     'quiet':"Don't print nonessential feedback", 
                     'timing':'Report execution times'}
                    self.hidden_commands = [
                     'eof', '_relative_load', '_relative_run_script']
                    self._persistent_history_length = persistent_history_length
                    self._initialize_history(persistent_history_file)
                    self.exclude_from_history = 'history edit eof'.split()
                    self.macros = dict()
                    self._pystate = {}
                    self._py_history = []
                    self.pyscript_name = 'app'
                    self.statement_parser = StatementParser(allow_redirection=allow_redirection, terminators=terminators,
                      multiline_commands=multiline_commands,
                      shortcuts=shortcuts)
                    self._in_py = False
                    self.last_result = None
                    self._script_dir = []
                    self.sigint_protection = utils.ContextFlag()
                    self._cur_pipe_proc_reader = None
                    self.completion_matches = []
                    self._redirecting = False
                    self._at_continuation_prompt = False
                    self.help_error = 'No help on {}'
                    self.default_error = '{} is not a recognized command, alias, or macro'
                    self.broken_pipe_warning = ''
                    self._startup_commands = []
                    if startup_script is not None:
                        startup_script = os.path.abspath(os.path.expanduser(startup_script))
                        if os.path.exists(startup_script):
                            if os.path.getsize(startup_script) > 0:
                                self._startup_commands.append("run_script '{}'".format(startup_script))
                        self._transcript_files = None
                        if allow_cli_args:
                            parser = argparse.ArgumentParser()
                            parser.add_argument('-t', '--test', action='store_true', help='Test against transcript(s) in FILE (wildcards OK)')
                            callopts, callargs = parser.parse_known_args()
                            if callopts.test:
                                self._transcript_files = callargs
                    elif callargs:
                        self._startup_commands.extend(callargs)
                else:
                    if transcript_files:
                        self._transcript_files = transcript_files
                    self.default_sort_key = ALPHABETICAL_SORT_KEY
                    self.allow_appended_space = True
                    self.allow_closing_quote = True
                    self.completion_header = ''
                    self.display_matches = []
                    self.matches_delimited = False
                    self.matches_sorted = False
                    if sys.platform.startswith('win'):
                        self.pager = self.pager_chop = 'more'
                    else:
                        self.pager = 'less -RXF'
                        self.pager_chop = 'less -SRXF'
                    self._can_clip = can_clip
                    self.exit_code = 0
                    self.terminal_lock = threading.RLock()
                    self.disabled_commands = dict()

            @property
            def allow_ansi(self) -> str:
                """Read-only property needed to support thgcmd_set when it reads allow_ansi"""
                return ansi.allow_ansi

            @allow_ansi.setter
            def allow_ansi(self, new_val: str) -> None:
                """Setter property needed to support thgcmd_set when it updates allow_ansi"""
                new_val = new_val.lower()
                if new_val == ansi.ANSI_TERMINAL.lower():
                    ansi.allow_ansi = ansi.ANSI_TERMINAL
                else:
                    if new_val == ansi.ANSI_ALWAYS.lower():
                        ansi.allow_ansi = ansi.ANSI_ALWAYS
                    else:
                        if new_val == ansi.ANSI_NEVER.lower():
                            ansi.allow_ansi = ansi.ANSI_NEVER
                        else:
                            self.perror('Invalid value: {} (valid values: {}, {}, {})'.format(new_val, ansi.ANSI_TERMINAL, ansi.ANSI_ALWAYS, ansi.ANSI_NEVER))

            @property
            def visible_prompt(self) -> str:
                """Read-only property to get the visible prompt with any ANSI escape codes stripped.

        Used by transcript testing to make it easier and more reliable when users are doing things like coloring the
        prompt using ANSI color codes.

        :return: prompt stripped of any ANSI escape codes
        """
                return ansi.strip_ansi(self.prompt)

            @property
            def aliases(self) -> Dict[(str, str)]:
                """Read-only property to access the aliases stored in the StatementParser."""
                return self.statement_parser.aliases

            @property
            def allow_redirection(self) -> bool:
                """Getter for the allow_redirection property that determines whether or not redirection of stdout is allowed."""
                return self.statement_parser.allow_redirection

            @allow_redirection.setter
            def allow_redirection(self, value: bool) -> None:
                """Setter for the allow_redirection property that determines whether or not redirection of stdout is allowed."""
                self.statement_parser.allow_redirection = value

            def poutput(self, msg: Any, *, end: str='\n') -> None:
                """Print message to self.stdout and appends a newline by default

        Also handles BrokenPipeError exceptions for when a commands's output has
        been piped to another process and that process terminates before the
        thgcmd command is finished executing.

        :param msg: message to print (anything convertible to a str with '{}'.format() is OK)
        :param end: string appended after the end of the message, default a newline
        """
                try:
                    ansi.ansi_aware_write(self.stdout, '{}{}'.format(msg, end))
                except BrokenPipeError:
                    if self.broken_pipe_warning:
                        sys.stderr.write(self.broken_pipe_warning)

            @staticmethod
            def perror(msg: Any, *, end: str='\n', apply_style: bool=True) -> None:
                """Print message to sys.stderr

        :param msg: message to print (anything convertible to a str with '{}'.format() is OK)
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ansi.style_error will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        """
                if apply_style:
                    final_msg = ansi.style_error(msg)
                else:
                    final_msg = '{}'.format(msg)
                ansi.ansi_aware_write(sys.stderr, final_msg + end)

            def pexcept(self, msg: Any, *, end: str='\n', apply_style: bool=True) -> None:
                """Print Exception message to sys.stderr. If debug is true, print exception traceback if one exists.

        :param msg: message or Exception to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ErrorStyle will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        """
                if self.debug:
                    if sys.exc_info() != (None, None, None):
                        import traceback
                        traceback.print_exc()
                else:
                    if isinstance(msg, Exception):
                        final_msg = "EXCEPTION of type '{}' occurred with message: '{}'".format(type(msg).__name__, msg)
                    else:
                        final_msg = '{}'.format(msg)
                    if apply_style:
                        final_msg = ansi.style_error(final_msg)
                    warning = self.debug or "\nTo enable full traceback, run the following command:  'set debug true'"
                    final_msg += ansi.style_warning(warning)
                self.perror(final_msg, end=end, apply_style=False)

            def pfeedback(self, msg: str) -> None:
                """For printing nonessential feedback.  Can be silenced with `quiet`.
           Inclusion in redirected output is controlled by `feedback_to_output`."""
                if not self.quiet:
                    if self.feedback_to_output:
                        self.poutput(msg)
                    else:
                        ansi.ansi_aware_write(sys.stderr, '{}\n'.format(msg))

            def ppaged(self, msg: str, end: str='\n', chop: bool=False) -> None:
                """Print output using a pager if it would go off screen and stdout isn't currently being redirected.

        Never uses a pager inside of a script (Python or text) or when output is being redirected or piped or when
        stdout or stdin are not a fully functional terminal.

        :param msg: message to print to current stdout (anything convertible to a str with '{}'.format() is OK)
        :param end: string appended after the end of the message if not already present, default a newline
        :param chop: True -> causes lines longer than the screen width to be chopped (truncated) rather than wrapped
                              - truncated text is still accessible by scrolling with the right & left arrow keys
                              - chopping is ideal for displaying wide tabular data as is done in utilities like pgcli
                     False -> causes lines longer than the screen width to wrap to the next line
                              - wrapping is ideal when you want to keep users from having to use horizontal scrolling

        WARNING: On Windows, the text always wraps regardless of what the chop argument is set to
        """
                import subprocess
                if msg is not None:
                    if msg != '':
                        try:
                            msg_str = '{}'.format(msg)
                            if not msg_str.endswith(end):
                                msg_str += end
                            else:
                                functional_terminal = False
                                if self.stdin.isatty():
                                    if self.stdout.isatty():
                                        if sys.platform.startswith('win') or os.environ.get('TERM') is not None:
                                            functional_terminal = True
                                if functional_terminal and not self._redirecting or self._in_py or self._script_dir:
                                    if ansi.allow_ansi.lower() == ansi.ANSI_NEVER.lower():
                                        msg_str = ansi.strip_ansi(msg_str)
                                    pager = self.pager
                                    if chop:
                                        pager = self.pager_chop
                                    with self.sigint_protection:
                                        pipe_proc = subprocess.Popen(pager, shell=True, stdin=(subprocess.PIPE))
                                        pipe_proc.communicate(msg_str.encode('utf-8', 'replace'))
                                else:
                                    ansi.ansi_aware_write(self.stdout, msg_str)
                        except BrokenPipeError:
                            if self.broken_pipe_warning:
                                sys.stderr.write(self.broken_pipe_warning)

            def _reset_completion_defaults(self) -> None:
                """
        Resets tab completion settings
        Needs to be called each time readline runs tab completion
        """
                self.allow_appended_space = True
                self.allow_closing_quote = True
                self.completion_header = ''
                self.display_matches = []
                self.matches_delimited = False
                self.matches_sorted = False
                if rl_type == RlType.GNU:
                    readline.set_completion_display_matches_hook(self._display_matches_gnu_readline)
                else:
                    if rl_type == RlType.PYREADLINE:
                        readline.rl.mode._display_completions = self._display_matches_pyreadline

            def tokens_for_completion(self, line: str, begidx: int, endidx: int) -> Tuple[(List[str], List[str])]:
                """Used by tab completion functions to get all tokens through the one being completed.

        :param line: the current input line with leading whitespace removed
        :param begidx: the beginning index of the prefix text
        :param endidx: the ending index of the prefix text
        :return: A 2 item tuple where the items are
                 **On Success**
                 - tokens: list of unquoted tokens - this is generally the list needed for tab completion functions
                 - raw_tokens: list of tokens with any quotes preserved = this can be used to know if a token was quoted
                 or is missing a closing quote
                 Both lists are guaranteed to have at least 1 item. The last item in both lists is the token being tab
                 completed
                 **On Failure**
                 - Two empty lists
        """
                import copy
                unclosed_quote = ''
                quotes_to_try = copy.copy(constants.QUOTES)
                tmp_line = line[:endidx]
                tmp_endidx = endidx
                while True:
                    try:
                        initial_tokens = shlex_split(tmp_line[:tmp_endidx])
                        if not unclosed_quote:
                            if begidx == tmp_endidx:
                                initial_tokens.append('')
                        break
                    except ValueError as ex:
                        try:
                            if str(ex) == 'No closing quotation' and quotes_to_try:
                                unclosed_quote = quotes_to_try[0]
                                quotes_to_try = quotes_to_try[1:]
                                tmp_line = line[:endidx]
                                tmp_line += unclosed_quote
                                tmp_endidx = endidx + 1
                            else:
                                return ([], [])
                        finally:
                            ex = None
                            del ex

                if self.allow_redirection:
                    raw_tokens = []
                    for cur_initial_token in initial_tokens:
                        if not len(cur_initial_token) <= 1:
                            if cur_initial_token[0] in constants.QUOTES:
                                raw_tokens.append(cur_initial_token)
                                continue
                            cur_index = 0
                            cur_char = cur_initial_token[cur_index]
                            cur_raw_token = ''
                            while True:
                                if cur_char not in constants.REDIRECTION_CHARS:
                                    while cur_char not in constants.REDIRECTION_CHARS:
                                        cur_raw_token += cur_char
                                        cur_index += 1
                                        if cur_index < len(cur_initial_token):
                                            cur_char = cur_initial_token[cur_index]
                                        else:
                                            break

                                else:
                                    redirect_char = cur_char
                                    while cur_char == redirect_char:
                                        cur_raw_token += cur_char
                                        cur_index += 1
                                        if cur_index < len(cur_initial_token):
                                            cur_char = cur_initial_token[cur_index]
                                        else:
                                            break

                                raw_tokens.append(cur_raw_token)
                                cur_raw_token = ''
                                if cur_index >= len(cur_initial_token):
                                    break

                else:
                    raw_tokens = initial_tokens
                tokens = [utils.strip_quotes(cur_token) for cur_token in raw_tokens]
                if unclosed_quote:
                    raw_tokens[-1] = raw_tokens[(-1)][:-1]
                return (tokens, raw_tokens)

            def delimiter_complete(self, text: str, line: str, begidx: int, endidx: int, match_against: Iterable, delimiter: str) -> List[str]:
                """
        Performs tab completion against a list but each match is split on a delimiter and only
        the portion of the match being tab completed is shown as the completion suggestions.
        This is useful if you match against strings that are hierarchical in nature and have a
        common delimiter.

        An easy way to illustrate this concept is path completion since paths are just directories/files
        delimited by a slash. If you are tab completing items in /home/user you don't get the following
        as suggestions:

        /home/user/file.txt     /home/user/program.c
        /home/user/maps/        /home/user/thgcmd.py

        Instead you are shown:

        file.txt                program.c
        maps/                   thgcmd.py

        For a large set of data, this can be visually more pleasing and easier to search.

        Another example would be strings formatted with the following syntax: company::department::name
        In this case the delimiter would be :: and the user could easily narrow down what they are looking
        for if they were only shown suggestions in the category they are at in the string.

        :param text: the string prefix we are attempting to match (all returned matches must begin with it)
        :param line: the current input line with leading whitespace removed
        :param begidx: the beginning index of the prefix text
        :param endidx: the ending index of the prefix text
        :param match_against: the list being matched against
        :param delimiter: what delimits each portion of the matches (ex: paths are delimited by a slash)
        :return: a list of possible tab completions
        """
                matches = utils.basic_complete(text, line, begidx, endidx, match_against)
                if matches:
                    self.matches_delimited = True
                    common_prefix = os.path.commonprefix(matches)
                    prefix_tokens = common_prefix.split(delimiter)
                    display_token_index = 0
                    if prefix_tokens:
                        display_token_index = len(prefix_tokens) - 1
                    for cur_match in matches:
                        match_tokens = cur_match.split(delimiter)
                        display_token = match_tokens[display_token_index]
                        if not display_token:
                            display_token = delimiter
                        self.display_matches.append(display_token)

                return matches

            def flag_based_complete(self, text: str, line: str, begidx: int, endidx: int, flag_dict: Dict[(str, Union[(Iterable, Callable)])], *, all_else: Union[(None, Iterable, Callable)]=None) -> List[str]:
                """Tab completes based on a particular flag preceding the token being completed.

        :param text: the string prefix we are attempting to match (all returned matches must begin with it)
        :param line: the current input line with leading whitespace removed
        :param begidx: the beginning index of the prefix text
        :param endidx: the ending index of the prefix text
        :param flag_dict: dictionary whose structure is the following:
                          `keys` - flags (ex: -c, --create) that result in tab completion for the next argument in the
                          command line
                          `values` - there are two types of values:
                          1. iterable list of strings to match against (dictionaries, lists, etc.)
                          2. function that performs tab completion (ex: path_complete)
        :param all_else: an optional parameter for tab completing any token that isn't preceded by a flag in flag_dict
        :return: a list of possible tab completions
        """
                tokens, _ = self.tokens_for_completion(line, begidx, endidx)
                if not tokens:
                    return []
                completions_matches = []
                match_against = all_else
                if len(tokens) > 1:
                    flag = tokens[(-2)]
                    if flag in flag_dict:
                        match_against = flag_dict[flag]
                elif isinstance(match_against, Iterable):
                    completions_matches = utils.basic_complete(text, line, begidx, endidx, match_against)
                else:
                    if callable(match_against):
                        completions_matches = match_against(text, line, begidx, endidx)
                return completions_matches

            def index_based_complete(self, text: str, line: str, begidx: int, endidx: int, index_dict: Mapping[(int, Union[(Iterable, Callable)])], *, all_else: Union[(None, Iterable, Callable)]=None) -> List[str]:
                """Tab completes based on a fixed position in the input string.

        :param text: the string prefix we are attempting to match (all returned matches must begin with it)
        :param line: the current input line with leading whitespace removed
        :param begidx: the beginning index of the prefix text
        :param endidx: the ending index of the prefix text
        :param index_dict: dictionary whose structure is the following:
                           `keys` - 0-based token indexes into command line that determine which tokens perform tab
                           completion
                           `values` - there are two types of values:
                           1. iterable list of strings to match against (dictionaries, lists, etc.)
                           2. function that performs tab completion (ex: path_complete)
        :param all_else: an optional parameter for tab completing any token that isn't at an index in index_dict
        :return: a list of possible tab completions
        """
                tokens, _ = self.tokens_for_completion(line, begidx, endidx)
                if not tokens:
                    return []
                else:
                    matches = []
                    index = len(tokens) - 1
                    if index in index_dict:
                        match_against = index_dict[index]
                    else:
                        match_against = all_else
                    if isinstance(match_against, Iterable):
                        matches = utils.basic_complete(text, line, begidx, endidx, match_against)
                    else:
                        if callable(match_against):
                            matches = match_against(text, line, begidx, endidx)
                return matches

            def path_complete(self, text: str, line: str, begidx: int, endidx: int, *, path_filter: Optional[Callable[([str], bool)]]=None) -> List[str]:
                """Performs completion of local file system paths

        :param text: the string prefix we are attempting to match (all returned matches must begin with it)
        :param line: the current input line with leading whitespace removed
        :param begidx: the beginning index of the prefix text
        :param endidx: the ending index of the prefix text
        :param path_filter: optional filter function that determines if a path belongs in the results
                            this function takes a path as its argument and returns True if the path should
                            be kept in the results
        :return: a list of possible tab completions
        """

                def complete_users():
                    self.allow_appended_space = False
                    self.allow_closing_quote = False
                    users = []
                    if sys.platform.startswith('win'):
                        expanded_path = os.path.expanduser(text)
                        if os.path.isdir(expanded_path):
                            user = text
                            if add_trailing_sep_if_dir:
                                user += os.path.sep
                            users.append(user)
                    else:
                        import pwd
                        for cur_pw in pwd.getpwall():
                            if os.path.isdir(cur_pw.pw_dir):
                                cur_user = '~' + cur_pw.pw_name
                                if cur_user.startswith(text):
                                    if add_trailing_sep_if_dir:
                                        cur_user += os.path.sep
                                    users.append(cur_user)

                    return users

                add_trailing_sep_if_dir = False
                if not endidx == len(line):
                    if endidx < len(line):
                        if line[endidx] != os.path.sep:
                            add_trailing_sep_if_dir = True
                    cwd = os.getcwd()
                    cwd_added = False
                    orig_tilde_path = ''
                    expanded_tilde_path = ''
                    search_str = text or os.path.join(os.getcwd(), '*')
                    cwd_added = True
                else:
                    wildcards = [
                     '*', '?']
                    for wildcard in wildcards:
                        if wildcard in text:
                            return []

                    search_str = text + '*'
                if text.startswith('~'):
                    sep_index = text.find(os.path.sep, 1)
                    if sep_index == -1:
                        return complete_users()
                    search_str = os.path.expanduser(search_str)
                    orig_tilde_path = text[:sep_index]
                    expanded_tilde_path = os.path.expanduser(orig_tilde_path)
                else:
                    if not os.path.dirname(text):
                        search_str = os.path.join(os.getcwd(), search_str)
                        cwd_added = True
                    else:
                        self.matches_delimited = True
                        matches = glob.glob(search_str)
                        if path_filter is not None:
                            matches = [c for c in matches if path_filter(c)]
                        elif len(matches) == 1:
                            if os.path.isdir(matches[0]):
                                self.allow_appended_space = False
                                self.allow_closing_quote = False
                            matches.sort(key=(self.default_sort_key))
                            self.matches_sorted = True
                            for index, cur_match in enumerate(matches):
                                self.display_matches.append(os.path.basename(cur_match))
                                if os.path.isdir(cur_match) and add_trailing_sep_if_dir:
                                    matches[index] += os.path.sep
                                    self.display_matches[index] += os.path.sep

                            if cwd_added:
                                if cwd == os.path.sep:
                                    to_replace = cwd
                        else:
                            to_replace = cwd + os.path.sep
                        matches = [cur_path.replace(to_replace, '', 1) for cur_path in matches]
                    if expanded_tilde_path:
                        matches = [cur_path.replace(expanded_tilde_path, orig_tilde_path, 1) for cur_path in matches]
                    return matches

            def shell_cmd_complete(self, text: str, line: str, begidx: int, endidx: int, *, complete_blank: bool=False) -> List[str]:
                """Performs completion of executables either in a user's path or a given path

        :param text: the string prefix we are attempting to match (all returned matches must begin with it)
        :param line: the current input line with leading whitespace removed
        :param begidx: the beginning index of the prefix text
        :param endidx: the ending index of the prefix text
        :param complete_blank: If True, then a blank will complete all shell commands in a user's path. If False, then
                               no completion is performed. Defaults to False to match Bash shell behavior.
        :return: a list of possible tab completions
        """
                if not complete_blank:
                    if not text:
                        return []
                if not text.startswith('~'):
                    if os.path.sep not in text:
                        return utils.get_exes_in_path(text)
                return self.path_complete(text, line, begidx, endidx, path_filter=(lambda path: os.path.isdir(path) or os.access(path, os.X_OK)))

            def _redirect_complete(self, text: str, line: str, begidx: int, endidx: int, compfunc: Callable) -> List[str]:
                """Called by complete() as the first tab completion function for all commands
        It determines if it should tab complete for redirection (|, >, >>) or use the
        completer function for the current command

        :param text: the string prefix we are attempting to match (all returned matches must begin with it)
        :param line: the current input line with leading whitespace removed
        :param begidx: the beginning index of the prefix text
        :param endidx: the ending index of the prefix text
        :param compfunc: the completer function for the current command
                         this will be called if we aren't completing for redirection
        :return: a list of possible tab completions
        """
                if self.allow_redirection:
                    _, raw_tokens = self.tokens_for_completion(line, begidx, endidx)
                    if not raw_tokens:
                        return []
                    if len(raw_tokens) > 1:
                        has_redirection = False
                        in_pipe = False
                        in_file_redir = False
                        thgcmd_shell_completion = False
                        thgcmd_path_completion = False
                        prior_token = None
                        for cur_token in raw_tokens:
                            if cur_token in constants.REDIRECTION_TOKENS:
                                has_redirection = True
                                if cur_token == constants.REDIRECTION_PIPE:
                                    if prior_token == constants.REDIRECTION_PIPE:
                                        return []
                                    in_pipe = True
                                    in_file_redir = False
                                else:
                                    if prior_token in constants.REDIRECTION_TOKENS or in_file_redir:
                                        return []
                                    in_pipe = False
                                    in_file_redir = True
                            else:
                                thgcmd_shell_completion = False
                                thgcmd_path_completion = False
                                if prior_token == constants.REDIRECTION_PIPE:
                                    thgcmd_shell_completion = True
                                else:
                                    if in_pipe or prior_token in (constants.REDIRECTION_OUTPUT, constants.REDIRECTION_APPEND):
                                        thgcmd_path_completion = True
                            prior_token = cur_token

                        if thgcmd_shell_completion:
                            return self.shell_cmd_complete(text, line, begidx, endidx)
                        if thgcmd_path_completion:
                            return self.path_complete(text, line, begidx, endidx)
                        if has_redirection:
                            return []
                return compfunc(text, line, begidx, endidx)

            @staticmethod
            def _pad_matches_to_display(matches_to_display: List[str]) -> Tuple[(List[str], int)]:
                """Adds padding to the matches being displayed as tab completion suggestions.
        The default padding of readline/pyreadine is small and not visually appealing
        especially if matches have spaces. It appears very squished together.

        :param matches_to_display: the matches being padded
        :return: the padded matches and length of padding that was added
        """
                if rl_type == RlType.GNU:
                    padding = '  '
                else:
                    if rl_type == RlType.PYREADLINE:
                        padding = '   '
                    else:
                        return (
                         matches_to_display, 0)
                return (
                 [cur_match + padding for cur_match in matches_to_display], len(padding))

            def _display_matches_gnu_readline(self, substitution: str, matches: List[str], longest_match_length: int) -> None:
                """Prints a match list using GNU readline's rl_display_match_list()
        This exists to print self.display_matches if it has data. Otherwise matches prints.

        :param substitution: the substitution written to the command line
        :param matches: the tab completion matches to display
        :param longest_match_length: longest printed length of the matches
        """
                if rl_type == RlType.GNU:
                    if self.display_matches:
                        matches_to_display = self.display_matches
                        longest_match_length = 0
                        for cur_match in matches_to_display:
                            cur_length = ansi.ansi_safe_wcswidth(cur_match)
                            if cur_length > longest_match_length:
                                longest_match_length = cur_length

                    else:
                        matches_to_display = matches
                    matches_to_display, padding_length = self._pad_matches_to_display(matches_to_display)
                    longest_match_length += padding_length
                    encoded_substitution = bytes(substitution, encoding='utf-8')
                    encoded_matches = [bytes(cur_match, encoding='utf-8') for cur_match in matches_to_display]
                    strings_array = (ctypes.c_char_p * (1 + len(encoded_matches) + 1))()
                    strings_array[0] = encoded_substitution
                    strings_array[1:-1] = encoded_matches
                    strings_array[-1] = None
                    if self.completion_header:
                        sys.stdout.write('\n' + self.completion_header)
                    readline_lib.rl_display_match_list(strings_array, len(encoded_matches), longest_match_length)
                    rl_force_redisplay()

            def _display_matches_pyreadline(self, matches: List[str]) -> None:
                """Prints a match list using pyreadline's _display_completions()
        This exists to print self.display_matches if it has data. Otherwise matches prints.

        :param matches: the tab completion matches to display
        """
                if rl_type == RlType.PYREADLINE:
                    if self.display_matches:
                        matches_to_display = self.display_matches
                    else:
                        matches_to_display = matches
                    matches_to_display, _ = self._pad_matches_to_display(matches_to_display)
                    if self.completion_header:
                        readline.rl.mode.console.write('\n' + self.completion_header)
                    orig_pyreadline_display(matches_to_display)

            def _complete_worker(self, text: str, state: int) -> Optional[str]:
                """The actual worker function for tab completion which is called by complete() and returns
        the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.

        This completer function is called as complete(text, state), for state in 0, 1, 2, …, until it returns a
        non-string value. It should return the next possible completion starting with text.

        :param text: the current word that user is typing
        :param state: non-negative integer
        """
                import functools
                if state == 0:
                    if rl_type != RlType.NONE:
                        unclosed_quote = ''
                        self._reset_completion_defaults()
                        orig_line = readline.get_line_buffer()
                        line = orig_line.lstrip()
                        stripped = len(orig_line) - len(line)
                        begidx = max(readline.get_begidx() - stripped, 0)
                        endidx = max(readline.get_endidx() - stripped, 0)
                        shortcut_to_restore = ''
                        if begidx == 0:
                            for shortcut, _ in self.statement_parser.shortcuts:
                                if text.startswith(shortcut):
                                    shortcut_to_restore = shortcut
                                    text = text[len(shortcut_to_restore):]
                                    begidx += len(shortcut_to_restore)
                                    break

                        if begidx > 0:
                            statement = self.statement_parser.parse_command_only(line)
                            command = statement.command
                            expanded_line = statement.command_and_args
                            rstripped_len = len(line) - len(line.rstrip())
                            expanded_line += ' ' * rstripped_len
                            if len(expanded_line) != len(line):
                                diff = len(expanded_line) - len(line)
                                begidx += diff
                                endidx += diff
                            line = expanded_line
                            tokens, raw_tokens = self.tokens_for_completion(line, begidx, endidx)
                            if len(tokens) <= 1:
                                self.completion_matches = []
                                return
                            text_to_remove = ''
                            raw_completion_token = raw_tokens[(-1)]
                            if raw_completion_token:
                                if raw_completion_token[0] in constants.QUOTES:
                                    unclosed_quote = raw_completion_token[0]
                                    actual_begidx = line[:endidx].rfind(tokens[(-1)])
                                    if actual_begidx != begidx:
                                        text_to_remove = line[actual_begidx:begidx]
                                        text = text_to_remove + text
                                        begidx = actual_begidx
                            if command in self.get_all_commands():
                                compfunc = getattr(self, 'complete_' + command, None)
                                if compfunc is None:
                                    func = self.cmd_func(command)
                                    if func and hasattr(func, 'argparser'):
                                        compfunc = functools.partial((self._autocomplete_default), argparser=(getattr(func, 'argparser')))
                    else:
                        compfunc = self.completedefault
                else:
                    if command in self.macros:
                        compfunc = self.path_complete
                    else:
                        if self.default_to_shell:
                            if command in utils.get_exes_in_path(command):
                                compfunc = self.path_complete
                            else:
                                compfunc = self.completedefault
                        else:
                            self.completion_matches = self._redirect_complete(text, line, begidx, endidx, compfunc)
                            if self.completion_matches:
                                self.completion_matches = utils.remove_duplicates(self.completion_matches)
                                self.display_matches = utils.remove_duplicates(self.display_matches)
                                if not self.display_matches:
                                    import copy
                                    self.display_matches = copy.copy(self.completion_matches)
                                else:
                                    add_quote = unclosed_quote or False
                                    common_prefix = os.path.commonprefix(self.completion_matches)
                                    if self.matches_delimited:
                                        display_prefix = os.path.commonprefix(self.display_matches)
                                        if not ' ' in common_prefix:
                                            if not display_prefix or any((' ' in match for match in self.display_matches)):
                                                add_quote = True
                                    elif common_prefix:
                                        if any((' ' in match for match in self.completion_matches)):
                                            add_quote = True
                                        if add_quote:
                                            if any(('"' in match for match in self.completion_matches)):
                                                unclosed_quote = "'"
                                    else:
                                        unclosed_quote = '"'
                                self.completion_matches = [unclosed_quote + match for match in self.completion_matches]
                            else:
                                if text_to_remove:
                                    self.completion_matches = [match.replace(text_to_remove, '', 1) for match in self.completion_matches]
                                elif shortcut_to_restore:
                                    self.completion_matches = [shortcut_to_restore + match for match in self.completion_matches]
                                else:
                                    self.completion_matches = utils.basic_complete(text, line, begidx, endidx, self._get_commands_aliases_and_macros_for_completion())
                        if len(self.completion_matches) == 1:
                            str_to_append = ''
                            if self.allow_closing_quote:
                                if unclosed_quote:
                                    str_to_append += unclosed_quote
                            if self.allow_appended_space:
                                if endidx == len(line):
                                    str_to_append += ' '
                            self.completion_matches[0] += str_to_append
                        if not self.matches_sorted:
                            self.completion_matches.sort(key=(self.default_sort_key))
                            self.display_matches.sort(key=(self.default_sort_key))
                            self.matches_sorted = True
                        try:
                            return self.completion_matches[state]
                        except IndexError:
                            return

            def complete(self, text: str, state: int) -> Optional[str]:
                """Override of thgcmd's complete method which returns the next possible completion for 'text'

        This method gets called directly by readline. Since readline suppresses any exception raised
        in completer functions, they can be difficult to debug. Therefore this function wraps the
        actual tab completion logic and prints to stderr any exception that occurs before returning
        control to readline.

        :param text: the current word that user is typing
        :param state: non-negative integer
        """
                try:
                    return self._complete_worker(text, state)
                except Exception as e:
                    try:
                        self.perror('\n', end='')
                        self.pexcept(e)
                        return
                    finally:
                        e = None
                        del e

            def _autocomplete_default(self, text: str, line: str, begidx: int, endidx: int, argparser: argparse.ArgumentParser) -> List[str]:
                """Default completion function for argparse commands"""
                from .argparse_completer import AutoCompleter
                completer = AutoCompleter(argparser, self)
                tokens, _ = self.tokens_for_completion(line, begidx, endidx)
                return completer.complete_command(tokens, text, line, begidx, endidx)

            def get_all_commands(self) -> List[str]:
                """Return a list of all commands"""
                return [name[len(COMMAND_FUNC_PREFIX):] for name in self.get_names() if name.startswith(COMMAND_FUNC_PREFIX) if callable(getattr(self, name))]

            def get_visible_commands(self) -> List[str]:
                """Return a list of commands that have not been hidden or disabled"""
                commands = self.get_all_commands()
                for name in self.hidden_commands:
                    if name in commands:
                        commands.remove(name)

                for name in self.disabled_commands:
                    if name in commands:
                        commands.remove(name)

                return commands

            def _get_alias_completion_items(self) -> List[CompletionItem]:
                """Return list of current alias names and values as CompletionItems"""
                return [CompletionItem(cur_key, self.aliases[cur_key]) for cur_key in self.aliases]

            def _get_macro_completion_items(self) -> List[CompletionItem]:
                """Return list of current macro names and values as CompletionItems"""
                return [CompletionItem(cur_key, self.macros[cur_key].value) for cur_key in self.macros]

            def _get_settable_completion_items(self) -> List[CompletionItem]:
                """Return list of current settable names and descriptions as CompletionItems"""
                return [CompletionItem(cur_key, self.settable[cur_key]) for cur_key in self.settable]

            def _get_commands_aliases_and_macros_for_completion(self) -> List[str]:
                """Return a list of visible commands, aliases, and macros for tab completion"""
                visible_commands = set(self.get_visible_commands())
                alias_names = set(self.aliases)
                macro_names = set(self.macros)
                return list(visible_commands | alias_names | macro_names)

            def get_help_topics(self) -> List[str]:
                """ Returns a list of help topics """
                return [name[len(HELP_FUNC_PREFIX):] for name in self.get_names() if name.startswith(HELP_FUNC_PREFIX) if callable(getattr(self, name))]

            def sigint_handler(self, signum: int, frame) -> None:
                """Signal handler for SIGINTs which typically come from Ctrl-C events.

        If you need custom SIGINT behavior, then override this function.

        :param signum: signal number
        :param frame: required param for signal handlers
        """
                if self._cur_pipe_proc_reader is not None:
                    self._cur_pipe_proc_reader.send_sigint()
                if not self.sigint_protection:
                    raise KeyboardInterrupt('Got a keyboard interrupt')

            def precmd(self, statement: Statement) -> Statement:
                """Hook method executed just before the command is processed by ``onecmd()`` and after adding it to the history.

        :param statement: subclass of str which also contains the parsed input
        :return: a potentially modified version of the input Statement object
        """
                return statement

            def parseline(self, line: str) -> Tuple[(str, str, str)]:
                """Parse the line into a command name and a string containing the arguments.

        NOTE: This is an override of a parent class method.  It is only used by other parent class methods.

        Different from the parent class method, this ignores self.identchars.

        :param line: line read by readline
        :return: tuple containing (command, args, line)
        """
                statement = self.statement_parser.parse_command_only(line)
                return (statement.command, statement.args, statement.command_and_args)

            def onecmd_plus_hooks(self, line: str, pyscript_bridge_call: bool=False) -> bool:
                """Top-level function called by cmdloop() to handle parsing a line and running the command and all of its hooks.

        :param line: line of text read from input
        :param pyscript_bridge_call: This should only ever be set to True by PyscriptBridge to signify the beginning
                                     of an app() call in a pyscript. It is used to enable/disable the storage of the
                                     command's stdout.
        :return: True if running of commands should stop
        """
                import datetime
                stop = False
                try:
                    statement = self._input_line_to_statement(line)
                except EmptyStatement:
                    return self._run_cmdfinalization_hooks(stop, None)
                except ValueError as ex:
                    try:
                        self.pexcept('Invalid syntax: {}'.format(ex))
                        return stop
                    finally:
                        ex = None
                        del ex

                try:
                    try:
                        data = plugin.PostparsingData(False, statement)
                        for func in self._postparsing_hooks:
                            data = func(data)
                            if data.stop:
                                break

                        statement = data.statement
                        stop = data.stop
                        if stop:
                            raise EmptyStatement
                        already_redirecting = self._redirecting
                        saved_state = None
                        try:
                            with self.sigint_protection:
                                if pyscript_bridge_call:
                                    self.stdout.pause_storage = False
                                redir_error, saved_state = self._redirect_output(statement)
                                self._cur_pipe_proc_reader = saved_state.pipe_proc_reader
                            if not redir_error:
                                if not already_redirecting:
                                    self._redirecting = saved_state.redirecting
                                timestart = datetime.datetime.now()
                                data = plugin.PrecommandData(statement)
                                for func in self._precmd_hooks:
                                    data = func(data)

                                statement = data.statement
                                statement = self.precmd(statement)
                                stop = self.onecmd(statement)
                                data = plugin.PostcommandData(stop, statement)
                                for func in self._postcmd_hooks:
                                    data = func(data)

                                stop = data.stop
                                stop = self.postcmd(stop, statement)
                                if self.timing:
                                    self.pfeedback('Elapsed: {}'.format(datetime.datetime.now() - timestart))
                        finally:
                            with self.sigint_protection:
                                if saved_state is not None:
                                    self._restore_output(statement, saved_state)
                                if not already_redirecting:
                                    self._redirecting = False
                                if pyscript_bridge_call:
                                    self.stdout.pause_storage = True

                    except EmptyStatement:
                        pass
                    except Exception as ex:
                        try:
                            self.pexcept(ex)
                        finally:
                            ex = None
                            del ex

                finally:
                    return

                return self._run_cmdfinalization_hooks(stop, statement)

            def _run_cmdfinalization_hooks(self, stop: bool, statement: Optional[Statement]) -> bool:
                """Run the command finalization hooks"""
                with self.sigint_protection:
                    if not sys.platform.startswith('win'):
                        if self.stdout.isatty():
                            import subprocess
                            proc = subprocess.Popen(['stty', 'sane'])
                            proc.communicate()
                try:
                    data = plugin.CommandFinalizationData(stop, statement)
                    for func in self._cmdfinalization_hooks:
                        data = func(data)

                    return data.stop
                except Exception as ex:
                    try:
                        self.pexcept(ex)
                    finally:
                        ex = None
                        del ex

            def runcmds_plus_hooks(self, cmds: List[Union[(HistoryItem, str)]]) -> bool:
                """
        Used when commands are being run in an automated fashion like text scripts or history replays.
        The prompt and command line for each command will be printed if echo is True.

        :param cmds: commands to run
        :return: True if running of commands should stop
        """
                for line in cmds:
                    if isinstance(line, HistoryItem):
                        line = line.raw
                    if self.echo:
                        self.poutput('{}{}'.format(self.prompt, line))
                    if self.onecmd_plus_hooks(line):
                        return True

                return False

            def _complete_statement(self, line: str) -> Statement:
                """Keep accepting lines of input until the command is complete.

        There is some pretty hacky code here to handle some quirks of
        self.pseuthgcmd_raw_input(). It returns a literal 'eof' if the input
        pipe runs out. We can't refactor it because we need to retain
        backwards compatibility with the standard library version of cmd.

        :param line: the line being parsed
        :return: the completed Statement
        """
                while True:
                    try:
                        statement = self.statement_parser.parse(line)
                        if statement.multiline_command:
                            if statement.terminator:
                                break
                        if not statement.multiline_command:
                            break
                    except ValueError:
                        statement = self.statement_parser.parse_command_only(line)
                        if not statement.multiline_command:
                            raise

                    try:
                        try:
                            self._at_continuation_prompt = True
                            newline = self._pseuthgcmd_raw_input(self.continuation_prompt)
                            if newline == 'eof':
                                newline = '\n'
                                self.poutput(newline)
                            line = '{}\n{}'.format(statement.raw, newline)
                        except KeyboardInterrupt as ex:
                            try:
                                if self.quit_on_sigint:
                                    raise ex
                                else:
                                    self.poutput('^C')
                                    statement = self.statement_parser.parse('')
                                    break
                            finally:
                                ex = None
                                del ex

                    finally:
                        self._at_continuation_prompt = False

                if not statement.command:
                    raise EmptyStatement()
                return statement

            def _input_line_to_statement(self, line: str) -> Statement:
                """
        Parse the user's input line and convert it to a Statement, ensuring that all macros are also resolved

        :param line: the line being parsed
        :return: parsed command line as a Statement
        """
                used_macros = []
                orig_line = None
                while 1:
                    statement = self._complete_statement(line)
                    if orig_line is None:
                        orig_line = statement.raw
                    if statement.command in self.macros.keys() and statement.command not in used_macros:
                        used_macros.append(statement.command)
                        line = self._resolve_macro(statement)
                        if line is None:
                            raise EmptyStatement()
                    else:
                        break

                if orig_line != statement.raw:
                    statement = Statement((statement.args), raw=orig_line,
                      command=(statement.command),
                      arg_list=(statement.arg_list),
                      multiline_command=(statement.multiline_command),
                      terminator=(statement.terminator),
                      suffix=(statement.suffix),
                      pipe_to=(statement.pipe_to),
                      output=(statement.output),
                      output_to=(statement.output_to))
                return statement

            def _resolve_macro(self, statement: Statement) -> Optional[str]:
                """
        Resolve a macro and return the resulting string

        :param statement: the parsed statement from the command line
        :return: the resolved macro or None on error
        """
                if statement.command not in self.macros.keys():
                    raise KeyError('{} is not a macro'.format(statement.command))
                macro = self.macros[statement.command]
                if len(statement.arg_list) < macro.minimum_arg_count:
                    self.perror("The macro '{}' expects at least {} argument(s)".format(statement.command, macro.minimum_arg_count))
                    return
                resolved = macro.value
                reverse_arg_list = sorted((macro.arg_list), key=(lambda ma: ma.start_index), reverse=True)
                for arg in reverse_arg_list:
                    if arg.is_escaped:
                        to_replace = '{{' + arg.number_str + '}}'
                        replacement = '{' + arg.number_str + '}'
                    else:
                        to_replace = '{' + arg.number_str + '}'
                        replacement = statement.argv[int(arg.number_str)]
                    parts = resolved.rsplit(to_replace, maxsplit=1)
                    resolved = parts[0] + replacement + parts[1]

                for arg in statement.arg_list[macro.minimum_arg_count:]:
                    resolved += ' ' + arg

                return resolved + statement.post_command

            def _redirect_output(self, statement: Statement) -> Tuple[(bool, utils.RedirectionSavedState)]:
                """Handles output redirection for >, >>, and |.

        :param statement: a parsed statement from the user
        :return: A bool telling if an error occurred and a utils.RedirectionSavedState object
        """
                import io, subprocess
                redir_error = False
                saved_state = utils.RedirectionSavedState(self.stdout, sys.stdout, self._cur_pipe_proc_reader)
                if not self.allow_redirection:
                    return (
                     redir_error, saved_state)
                    if statement.pipe_to:
                        read_fd, write_fd = os.pipe()
                        subproc_stdin = io.open(read_fd, 'r')
                        new_stdout = io.open(write_fd, 'w')
                        if sys.platform == 'win32':
                            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
                            start_new_session = False
                        else:
                            creationflags = 0
                            start_new_session = True
                        proc = subprocess.Popen((statement.pipe_to), stdin=subproc_stdin,
                          stdout=(subprocess.PIPE if isinstance(self.stdout, utils.StdSim) else self.stdout),
                          stderr=(subprocess.PIPE if isinstance(sys.stderr, utils.StdSim) else sys.stderr),
                          creationflags=creationflags,
                          start_new_session=start_new_session,
                          shell=True)
                        try:
                            proc.wait(0.2)
                        except subprocess.TimeoutExpired:
                            pass

                        if proc.returncode is not None:
                            self.perror('Pipe process exited with code {} before command could run'.format(proc.returncode))
                            subproc_stdin.close()
                            new_stdout.close()
                            redir_error = True
                    else:
                        saved_state.redirecting = True
                        saved_state.pipe_proc_reader = utils.ProcReader(proc, self.stdout, sys.stderr)
                        sys.stdout = self.stdout = new_stdout
                else:
                    pass
                if statement.output:
                    import tempfile
                    statement.output_to or self._can_clip or self.perror("Cannot redirect to paste buffer; install 'pyperclip' and re-run to enable")
                    redir_error = True
                else:
                    if statement.output_to:
                        mode = 'w'
                        if statement.output == constants.REDIRECTION_APPEND:
                            mode = 'a'
                        try:
                            new_stdout = open(utils.strip_quotes(statement.output_to), mode)
                            saved_state.redirecting = True
                            sys.stdout = self.stdout = new_stdout
                        except OSError as ex:
                            try:
                                self.pexcept('Failed to redirect because - {}'.format(ex))
                                redir_error = True
                            finally:
                                ex = None
                                del ex

                    else:
                        new_stdout = tempfile.TemporaryFile(mode='w+')
                        saved_state.redirecting = True
                        sys.stdout = self.stdout = new_stdout
                        if statement.output == constants.REDIRECTION_APPEND:
                            self.poutput(get_paste_buffer())
                        return (redir_error, saved_state)

            def _restore_output(self, statement: Statement, saved_state: utils.RedirectionSavedState) -> None:
                """Handles restoring state after output redirection as well as
        the actual pipe operation if present.

        :param statement: Statement object which contains the parsed input from the user
        :param saved_state: contains information needed to restore state data
        """
                if saved_state.redirecting:
                    if statement.output:
                        if not statement.output_to:
                            self.stdout.seek(0)
                            write_to_paste_buffer(self.stdout.read())
                    try:
                        self.stdout.close()
                    except BrokenPipeError:
                        pass

                    self.stdout = saved_state.saved_self_stdout
                    sys.stdout = saved_state.saved_sys_stdout
                    if self._cur_pipe_proc_reader is not None:
                        self._cur_pipe_proc_reader.wait()
                self._cur_pipe_proc_reader = saved_state.saved_pipe_proc_reader

            def cmd_func(self, command: str) -> Optional[Callable]:
                """
        Get the function for a command
        :param command: the name of the command
        """
                func_name = self._cmd_func_name(command)
                if func_name:
                    return getattr(self, func_name)

            def _cmd_func_name(self, command: str) -> str:
                """Get the method name associated with a given command.

        :param command: command to look up method name which implements it
        :return: method name which implements the given command
        """
                target = COMMAND_FUNC_PREFIX + command
                if callable(getattr(self, target, None)):
                    return target
                return ''

            def onecmd(self, statement: Union[(Statement, str)]) -> bool:
                """ This executes the actual thgcmd_* method for a command.

        If the command provided doesn't exist, then it executes default() instead.

        :param statement: intended to be a Statement instance parsed command from the input stream, alternative
                          acceptance of a str is present only for backward compatibility with cmd
        :return: a flag indicating whether the interpretation of commands should stop
        """
                if not isinstance(statement, Statement):
                    statement = self._input_line_to_statement(statement)
                else:
                    func = self.cmd_func(statement.command)
                    if func:
                        if statement.command not in self.exclude_from_history:
                            if statement.command not in self.disabled_commands:
                                self.history.append(statement)
                        stop = func(statement)
                    else:
                        stop = self.default(statement)
                if stop is None:
                    stop = False
                return stop

            def default(self, statement: Statement) -> Optional[bool]:
                """Executed when the command given isn't a recognized command implemented by a thgcmd_* method.

        :param statement: Statement object with parsed input
        """
                if self.default_to_shell:
                    if 'shell' not in self.exclude_from_history:
                        self.history.append(statement)
                    return self.thgcmd_shell(statement.command_and_args)
                err_msg = self.default_error.format(statement.command)
                ansi.ansi_aware_write(sys.stderr, '{}\n'.format(err_msg))

            def _pseuthgcmd_raw_input(self, prompt: str) -> str:
                """Began life as a copy of cmd's cmdloop; like raw_input but

        - accounts for changed stdin, stdout
        - if input is a pipe (instead of a tty), look at self.echo
          to decide whether to print the prompt and the input
        """
                if self.use_rawinput:
                    try:
                        try:
                            if sys.stdin.isatty():
                                try:
                                    self.terminal_lock.release()
                                except RuntimeError:
                                    pass

                                safe_prompt = rl_make_safe_prompt(prompt)
                                line = input(safe_prompt)
                            else:
                                line = input()
                                if self.echo:
                                    sys.stdout.write('{}{}\n'.format(prompt, line))
                        except EOFError:
                            line = 'eof'

                    finally:
                        if sys.stdin.isatty():
                            self.terminal_lock.acquire()

                else:
                    if self.stdin.isatty():
                        self.poutput(prompt, end='')
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if len(line) == 0:
                            line = 'eof'
                    else:
                        line = self.stdin.readline()
                        if len(line):
                            if self.echo:
                                self.poutput('{}{}'.format(prompt, line))
                        else:
                            line = 'eof'
                return line.strip()

            def _cmdloop(self) -> None:
                """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        This serves the same role as cmd.cmdloop().
        """
                if self.use_rawinput:
                    if self.completekey:
                        if rl_type != RlType.NONE:
                            if rl_type == RlType.GNU:
                                saved_basic_quotes = ctypes.cast(rl_basic_quote_characters, ctypes.c_void_p).value
                                rl_basic_quote_characters.value = None
                            saved_completer = readline.get_completer()
                            readline.set_completer(self.complete)
                            completer_delims = ' \t\n' + ''.join(constants.QUOTES)
                            if self.allow_redirection:
                                completer_delims += ''.join(constants.REDIRECTION_CHARS)
                            saved_delims = readline.get_completer_delims()
                            readline.set_completer_delims(completer_delims)
                            readline.parse_and_bind(self.completekey + ': complete')
                try:
                    stop = self.runcmds_plus_hooks(self._startup_commands)
                    self._startup_commands.clear()
                    while not stop:
                        try:
                            line = self._pseuthgcmd_raw_input(self.prompt)
                        except KeyboardInterrupt as ex:
                            try:
                                if self.quit_on_sigint:
                                    raise ex
                                else:
                                    self.poutput('^C')
                                    line = ''
                            finally:
                                ex = None
                                del ex

                        stop = self.onecmd_plus_hooks(line)

                finally:
                    if self.use_rawinput:
                        if self.completekey:
                            if rl_type != RlType.NONE:
                                readline.set_completer(saved_completer)
                                readline.set_completer_delims(saved_delims)
                                if rl_type == RlType.GNU:
                                    readline.set_completion_display_matches_hook(None)
                                    rl_basic_quote_characters.value = saved_basic_quotes
                                else:
                                    if rl_type == RlType.PYREADLINE:
                                        readline.rl.mode._display_completions = orig_pyreadline_display

            def _alias_create(self, args: argparse.Namespace) -> None:
                """Create or overwrite an alias"""
                valid, errmsg = self.statement_parser.is_valid_command(args.name)
                if not valid:
                    self.perror('Invalid alias name: {}'.format(errmsg))
                    return
                if args.name in self.macros:
                    self.perror('Alias cannot have the same name as a macro')
                    return
                tokens_to_unquote = constants.REDIRECTION_TOKENS
                tokens_to_unquote.extend(self.statement_parser.terminators)
                utils.unquote_specific_tokens(args.command_args, tokens_to_unquote)
                value = args.command
                if args.command_args:
                    value += ' ' + ' '.join(args.command_args)
                result = 'overwritten' if args.name in self.aliases else 'created'
                self.aliases[args.name] = value
                self.poutput("Alias '{}' {}".format(args.name, result))

            def _alias_delete(self, args: argparse.Namespace) -> None:
                """Delete aliases"""
                if args.all:
                    self.aliases.clear()
                    self.poutput('All aliases deleted')
                else:
                    if not args.name:
                        self.thgcmd_help('alias delete')
                    else:
                        for cur_name in utils.remove_duplicates(args.name):
                            if cur_name in self.aliases:
                                del self.aliases[cur_name]
                                self.poutput("Alias '{}' deleted".format(cur_name))
                            else:
                                self.perror("Alias '{}' does not exist".format(cur_name))

            def _alias_list(self, args: argparse.Namespace) -> None:
                """List some or all aliases"""
                if args.name:
                    for cur_name in utils.remove_duplicates(args.name):
                        if cur_name in self.aliases:
                            self.poutput('alias create {} {}'.format(cur_name, self.aliases[cur_name]))
                        else:
                            self.perror("Alias '{}' not found".format(cur_name))

                else:
                    for cur_alias in sorted((self.aliases), key=(self.default_sort_key)):
                        self.poutput('alias create {} {}'.format(cur_alias, self.aliases[cur_alias]))

            alias_description = 'Manage aliases\n\nAn alias is a command that enables replacement of a word by another string.'
            alias_epilog = 'See also:\n  macro'
            alias_parser = ArgParser(description=alias_description, epilog=alias_epilog, prog='alias')
            alias_subparsers = alias_parser.add_subparsers()
            alias_create_help = 'create or overwrite an alias'
            alias_create_description = 'Create or overwrite an alias'
            alias_create_epilog = 'Notes:\n  If you want to use redirection, pipes, or terminators like \';\' in the value\n  of the alias, then quote them.\n\n  Since aliases are resolved during parsing, tab completion will function as\n  it would for the actual command the alias resolves to.\n\nExamples:\n  alias create ls !ls -lF\n  alias create show_log !cat "log file.txt"\n  alias create save_results print_results ">" out.txt\n'
            alias_create_parser = alias_subparsers.add_parser('create', help=alias_create_help, description=alias_create_description,
              epilog=alias_create_epilog)
            alias_create_parser.add_argument('name', help='name of this alias')
            alias_create_parser.add_argument('command', help='what the alias resolves to', choices_method=_get_commands_aliases_and_macros_for_completion)
            alias_create_parser.add_argument('command_args', nargs=(argparse.REMAINDER), help='arguments to pass to command', completer_method=path_complete)
            alias_create_parser.set_defaults(func=_alias_create)
            alias_delete_help = 'delete aliases'
            alias_delete_description = 'Delete specified aliases or all aliases if --all is used'
            alias_delete_parser = alias_subparsers.add_parser('delete', help=alias_delete_help, description=alias_delete_description)
            alias_delete_parser.add_argument('name', nargs=(argparse.ZERO_OR_MORE), help='alias to delete', choices_method=_get_alias_completion_items,
              descriptive_header='Value')
            alias_delete_parser.add_argument('-a', '--all', action='store_true', help='delete all aliases')
            alias_delete_parser.set_defaults(func=_alias_delete)
            alias_list_help = 'list aliases'
            alias_list_description = 'List specified aliases in a reusable form that can be saved to a startup\nscript to preserve aliases across sessions\n\nWithout arguments, all aliases will be listed.'
            alias_list_parser = alias_subparsers.add_parser('list', help=alias_list_help, description=alias_list_description)
            alias_list_parser.add_argument('name', nargs=(argparse.ZERO_OR_MORE), help='alias to list', choices_method=_get_alias_completion_items,
              descriptive_header='Value')
            alias_list_parser.set_defaults(func=_alias_list)

            @with_argparser(alias_parser, preserve_quotes=True)
            def thgcmd_alias(self, args: argparse.Namespace) -> None:
                """Manage aliases"""
                func = getattr(args, 'func', None)
                if func is not None:
                    func(self, args)
                else:
                    self.thgcmd_help('alias')

            def _macro_create(self, args: argparse.Namespace) -> None:
                """Create or overwrite a macro"""
                valid, errmsg = self.statement_parser.is_valid_command(args.name)
                if not valid:
                    self.perror('Invalid macro name: {}'.format(errmsg))
                    return
                if args.name in self.get_all_commands():
                    self.perror('Macro cannot have the same name as a command')
                    return
                if args.name in self.aliases:
                    self.perror('Macro cannot have the same name as an alias')
                    return
                tokens_to_unquote = constants.REDIRECTION_TOKENS
                tokens_to_unquote.extend(self.statement_parser.terminators)
                utils.unquote_specific_tokens(args.command_args, tokens_to_unquote)
                value = args.command
                if args.command_args:
                    value += ' ' + ' '.join(args.command_args)
                arg_list = []
                normal_matches = re.finditer(MacroArg.macro_normal_arg_pattern, value)
                max_arg_num = 0
                arg_nums = set()
                while True:
                    try:
                        cur_match = normal_matches.__next__()
                        cur_num_str = re.findall(MacroArg.digit_pattern, cur_match.group())[0]
                        cur_num = int(cur_num_str)
                        if cur_num < 1:
                            self.perror('Argument numbers must be greater than 0')
                            return
                        arg_nums.add(cur_num)
                        if cur_num > max_arg_num:
                            max_arg_num = cur_num
                        arg_list.append(MacroArg(start_index=(cur_match.start()), number_str=cur_num_str, is_escaped=False))
                    except StopIteration:
                        break

                if len(arg_nums) != max_arg_num:
                    self.perror('Not all numbers between 1 and {} are present in the argument placeholders'.format(max_arg_num))
                    return
                escaped_matches = re.finditer(MacroArg.macro_escaped_arg_pattern, value)
                while True:
                    try:
                        cur_match = escaped_matches.__next__()
                        cur_num_str = re.findall(MacroArg.digit_pattern, cur_match.group())[0]
                        arg_list.append(MacroArg(start_index=(cur_match.start()), number_str=cur_num_str, is_escaped=True))
                    except StopIteration:
                        break

                result = 'overwritten' if args.name in self.macros else 'created'
                self.macros[args.name] = Macro(name=(args.name), value=value, minimum_arg_count=max_arg_num, arg_list=arg_list)
                self.poutput("Macro '{}' {}".format(args.name, result))

            def _macro_delete(self, args: argparse.Namespace) -> None:
                """Delete macros"""
                if args.all:
                    self.macros.clear()
                    self.poutput('All macros deleted')
                else:
                    if not args.name:
                        self.thgcmd_help('macro delete')
                    else:
                        for cur_name in utils.remove_duplicates(args.name):
                            if cur_name in self.macros:
                                del self.macros[cur_name]
                                self.poutput("Macro '{}' deleted".format(cur_name))
                            else:
                                self.perror("Macro '{}' does not exist".format(cur_name))

            def _macro_list(self, args: argparse.Namespace) -> None:
                """List some or all macros"""
                if args.name:
                    for cur_name in utils.remove_duplicates(args.name):
                        if cur_name in self.macros:
                            self.poutput('macro create {} {}'.format(cur_name, self.macros[cur_name].value))
                        else:
                            self.perror("Macro '{}' not found".format(cur_name))

                else:
                    for cur_macro in sorted((self.macros), key=(self.default_sort_key)):
                        self.poutput('macro create {} {}'.format(cur_macro, self.macros[cur_macro].value))

            macro_description = 'Manage macros\n\nA macro is similar to an alias, but it can contain argument placeholders.'
            macro_epilog = 'See also:\n  alias'
            macro_parser = ArgParser(description=macro_description, epilog=macro_epilog, prog='macro')
            macro_subparsers = macro_parser.add_subparsers()
            macro_create_help = 'create or overwrite a macro'
            macro_create_description = 'Create or overwrite a macro'
            macro_create_epilog = 'A macro is similar to an alias, but it can contain argument placeholders.\nArguments are expressed when creating a macro using {#} notation where {1}\nmeans the first argument.\n\nThe following creates a macro called my_macro that expects two arguments:\n\n  macro create my_macro make_dinner --meat {1} --veggie {2}\n\nWhen the macro is called, the provided arguments are resolved and the\nassembled command is run. For example:\n\n  my_macro beef broccoli ---> make_dinner --meat beef --veggie broccoli\n\nNotes:\n  To use the literal string {1} in your command, escape it this way: {{1}}.\n\n  Extra arguments passed to a macro are appended to resolved command.\n\n  An argument number can be repeated in a macro. In the following example the\n  first argument will populate both {1} instances.\n\n    macro create ft file_taxes -p {1} -q {2} -r {1}\n\n  To quote an argument in the resolved command, quote it during creation.\n\n    macro create backup !cp "{1}" "{1}.orig"\n\n  If you want to use redirection, pipes, or terminators like \';\' in the value\n  of the macro, then quote them.\n\n    macro create show_results print_results -type {1} "|" less\n\n  Because macros do not resolve until after hitting Enter, tab completion\n  will only complete paths while entering a macro.'
            macro_create_parser = macro_subparsers.add_parser('create', help=macro_create_help, description=macro_create_description,
              epilog=macro_create_epilog)
            macro_create_parser.add_argument('name', help='name of this macro')
            macro_create_parser.add_argument('command', help='what the macro resolves to', choices_method=_get_commands_aliases_and_macros_for_completion)
            macro_create_parser.add_argument('command_args', nargs=(argparse.REMAINDER), help='arguments to pass to command',
              completer_method=path_complete)
            macro_create_parser.set_defaults(func=_macro_create)
            macro_delete_help = 'delete macros'
            macro_delete_description = 'Delete specified macros or all macros if --all is used'
            macro_delete_parser = macro_subparsers.add_parser('delete', help=macro_delete_help, description=macro_delete_description)
            macro_delete_parser.add_argument('name', nargs=(argparse.ZERO_OR_MORE), help='macro to delete', choices_method=_get_macro_completion_items,
              descriptive_header='Value')
            macro_delete_parser.add_argument('-a', '--all', action='store_true', help='delete all macros')
            macro_delete_parser.set_defaults(func=_macro_delete)
            macro_list_help = 'list macros'
            macro_list_description = 'List specified macros in a reusable form that can be saved to a startup script\nto preserve macros across sessions\n\nWithout arguments, all macros will be listed.'
            macro_list_parser = macro_subparsers.add_parser('list', help=macro_list_help, description=macro_list_description)
            macro_list_parser.add_argument('name', nargs=(argparse.ZERO_OR_MORE), help='macro to list', choices_method=_get_macro_completion_items,
              descriptive_header='Value')
            macro_list_parser.set_defaults(func=_macro_list)

            @with_argparser(macro_parser, preserve_quotes=True)
            def thgcmd_macro(self, args: argparse.Namespace) -> None:
                """Manage macros"""
                func = getattr(args, 'func', None)
                if func is not None:
                    func(self, args)
                else:
                    self.thgcmd_help('macro')

            def complete_help_command(self, text: str, line: str, begidx: int, endidx: int) -> List[str]:
                """Completes the command argument of help"""
                topics = set(self.get_help_topics())
                visible_commands = set(self.get_visible_commands())
                strs_to_match = list(topics | visible_commands)
                return utils.basic_complete(text, line, begidx, endidx, strs_to_match)

            def complete_help_subcommand(self, text: str, line: str, begidx: int, endidx: int) -> List[str]:
                """Completes the subcommand argument of help"""
                tokens, _ = self.tokens_for_completion(line, begidx, endidx)
                if not tokens:
                    return []
                if len(tokens) < 3:
                    return []
                cmd_index = 1
                for cur_token in tokens[cmd_index:]:
                    if not cur_token.startswith('-'):
                        break
                    cmd_index += 1

                if cmd_index >= len(tokens):
                    return []
                command = tokens[cmd_index]
                matches = []
                func = self.cmd_func(command)
                if func:
                    if hasattr(func, 'argparser'):
                        from .argparse_completer import AutoCompleter
                        completer = AutoCompleter(getattr(func, 'argparser'), self)
                        matches = completer.complete_command_help(tokens[cmd_index:], text, line, begidx, endidx)
                return matches

            help_parser = ArgParser()
            help_parser.add_argument('command', nargs=(argparse.OPTIONAL), help='command to retrieve help for', completer_method=complete_help_command)
            help_parser.add_argument('subcommand', nargs=(argparse.REMAINDER), help='sub-command to retrieve help for', completer_method=complete_help_subcommand)
            help_parser.add_argument('-v', '--verbose', action='store_true', help='print a list of all commands with descriptions of each')
            if getattr(cmd.Cmd, 'complete_help', None) is not None:
                delattr(cmd.Cmd, 'complete_help')

            @with_argparser(help_parser)
            def thgcmd_help(self, args):
                """List available commands or provide detailed help for a specific command"""
                if not args.command or args.verbose:
                    self._help_menu(args.verbose)
                else:
                    func = self.cmd_func(args.command)
                    help_func = getattr(self, HELP_FUNC_PREFIX + args.command, None)
                    if func and hasattr(func, 'argparser'):
                        from .argparse_completer import AutoCompleter
                        completer = AutoCompleter(getattr(func, 'argparser'), self)
                        tokens = [args.command] + args.subcommand
                        self.poutput(completer.format_help(tokens))
                    else:
                        if help_func is None:
                            err_msg = func is None or func.__doc__ or self.help_error.format(args.command)
                            ansi.ansi_aware_write(sys.stderr, '{}\n'.format(err_msg))
                        else:
                            super().thgcmd_help(args.command)

            def _help_menu(self, verbose: bool=False) -> None:
                """Show a list of commands which help can be displayed for.
        """
                help_topics = sorted((self.get_help_topics()), key=(self.default_sort_key))
                visible_commands = sorted((self.get_visible_commands()), key=(self.default_sort_key))
                cmds_doc = []
                cmds_undoc = []
                cmds_cats = {}
                for command in visible_commands:
                    func = self.cmd_func(command)
                    has_help_func = False
                    if command in help_topics:
                        help_topics.remove(command)
                        if not hasattr(func, 'argparser'):
                            has_help_func = True
                    if hasattr(func, HELP_CATEGORY):
                        category = getattr(func, HELP_CATEGORY)
                        cmds_cats.setdefault(category, [])
                        cmds_cats[category].append(command)
                    elif func.__doc__ or has_help_func:
                        cmds_doc.append(command)
                    else:
                        cmds_undoc.append(command)

                if len(cmds_cats) == 0:
                    self.poutput('{}'.format(str(self.doc_leader)))
                    self._print_topics(self.doc_header, cmds_doc, verbose)
                else:
                    self.poutput('{}'.format(str(self.doc_leader)))
                    self.poutput(('{}'.format(str(self.doc_header))), end='\n\n')
                    for category in sorted((cmds_cats.keys()), key=(self.default_sort_key)):
                        self._print_topics(category, cmds_cats[category], verbose)

                    self._print_topics('Other', cmds_doc, verbose)
                self.print_topics(self.misc_header, help_topics, 15, 80)
                self.print_topics(self.undoc_header, cmds_undoc, 15, 80)

            def _print_topics(self, header: str, cmds: List[str], verbose: bool) -> None:
                """Customized version of print_topics that can switch between verbose or traditional output"""
                import io
                if cmds:
                    if not verbose:
                        self.print_topics(header, cmds, 15, 80)
                    else:
                        self.stdout.write('{}\n'.format(str(header)))
                        widest = 0
                        for command in cmds:
                            width = ansi.ansi_safe_wcswidth(command)
                            if width > widest:
                                widest = width

                        widest += 4
                        if widest < 20:
                            widest = 20
                        if self.ruler:
                            self.stdout.write('{:{ruler}<{width}}\n'.format('', ruler=(self.ruler), width=80))
                        topics = self.get_help_topics()
                        for command in cmds:
                            cmd_func = self.cmd_func(command)
                            if not hasattr(cmd_func, 'argparser'):
                                if command in topics:
                                    help_func = getattr(self, HELP_FUNC_PREFIX + command)
                                    result = io.StringIO()
                                    with redirect_stdout(result):
                                        stdout_orig = self.stdout
                                        try:
                                            self.stdout = result
                                            help_func()
                                        finally:
                                            self.stdout = stdout_orig

                                    doc = result.getvalue()
                                else:
                                    doc = cmd_func.__doc__
                                if not doc:
                                    doc_block = [
                                     '']
                                else:
                                    doc_block = []
                                    found_first = False
                                    for doc_line in doc.splitlines():
                                        stripped_line = doc_line.strip()
                                        if stripped_line.startswith(':'):
                                            if found_first:
                                                break
                                            elif stripped_line:
                                                doc_block.append(stripped_line)
                                                found_first = True
                                            elif found_first:
                                                break

                                for doc_line in doc_block:
                                    self.stdout.write('{: <{col_width}}{doc}\n'.format(command, col_width=widest,
                                      doc=doc_line))
                                    command = ''

                        self.stdout.write('\n')

            @with_argparser(ArgParser())
            def thgcmd_shortcuts(self, _: argparse.Namespace) -> None:
                """List available shortcuts"""
                sorted_shortcuts = sorted((self.statement_parser.shortcuts), key=(lambda x: self.default_sort_key(x[0])))
                result = '\n'.join(('{}: {}'.format(sc[0], sc[1]) for sc in sorted_shortcuts))
                self.poutput('Shortcuts for other commands:\n{}'.format(result))

            @with_argparser(ArgParser(epilog=INTERNAL_COMMAND_EPILOG))
            def thgcmd_eof(self, _: argparse.Namespace) -> bool:
                """Called when <Ctrl>-D is pressed"""
                return True

            @with_argparser(ArgParser())
            def thgcmd_quit(self, _: argparse.Namespace) -> bool:
                """Exit this application"""
                return True

            def select(self, opts: Union[(str, List[str], List[Tuple[(Any, Optional[str])]])], prompt: str='Your choice? ') -> str:
                """Presents a numbered menu to the user.  Modeled after
           the bash shell's SELECT.  Returns the item chosen.

           Argument ``opts`` can be:

             | a single string -> will be split into one-word options
             | a list of strings -> will be offered as options
             | a list of tuples -> interpreted as (value, text), so
                                   that the return value can differ from
                                   the text advertised to the user """
                local_opts = opts
                if isinstance(opts, str):
                    local_opts = list(zip(opts.split(), opts.split()))
                fulloptions = []
                for opt in local_opts:
                    if isinstance(opt, str):
                        fulloptions.append((opt, opt))
                    else:
                        try:
                            fulloptions.append((opt[0], opt[1]))
                        except IndexError:
                            fulloptions.append((opt[0], opt[0]))

                for idx, (_, text) in enumerate(fulloptions):
                    self.poutput('  %2d. %s' % (idx + 1, text))

                while True:
                    safe_prompt = rl_make_safe_prompt(prompt)
                    response = input(safe_prompt)
                    if rl_type != RlType.NONE:
                        hlen = readline.get_current_history_length()
                        if hlen >= 1:
                            if response != '':
                                readline.remove_history_item(hlen - 1)
                    try:
                        choice = int(response)
                        if choice < 1:
                            raise IndexError
                        result = fulloptions[(choice - 1)][0]
                        break
                    except (ValueError, IndexError):
                        self.poutput("{!r} isn't a valid choice. Pick a number between 1 and {}:".format(response, len(fulloptions)))

                return result

            def _cmdenvironment(self) -> str:
                """Get a summary report of read-only settings which the user cannot modify at runtime.

        :return: summary report of read-only settings which the user cannot modify at runtime
        """
                read_only_settings = '\n        Commands may be terminated with: {}\n        Output redirection and pipes allowed: {}'
                return read_only_settings.format(str(self.statement_parser.terminators), self.allow_redirection)

            def _show(self, args: argparse.Namespace, parameter: str='') -> None:
                """Shows current settings of parameters.

        :param args: argparse parsed arguments from the set command
        :param parameter: optional search parameter
        """
                param = utils.norm_fold(parameter.strip())
                result = {}
                maxlen = 0
                for p in self.settable:
                    if not param or p.startswith(param):
                        result[p] = '{}: {}'.format(p, str(getattr(self, p)))
                        maxlen = max(maxlen, len(result[p]))

                if result:
                    for p in sorted(result, key=(self.default_sort_key)):
                        if args.long:
                            self.poutput('{} # {}'.format(result[p].ljust(maxlen), self.settable[p]))
                        else:
                            self.poutput(result[p])

                    if args.all:
                        self.poutput('\nRead only settings:{}'.format(self._cmdenvironment()))
                else:
                    self.perror("Parameter '{}' not supported (type 'set' for list of parameters).".format(param))

            set_description = 'Set a settable parameter or show current settings of parameters\n\nAccepts abbreviated parameter names so long as there is no ambiguity.\nCall without arguments for a list of settable parameters with their values.'
            set_parser = ArgParser(description=set_description)
            set_parser.add_argument('-a', '--all', action='store_true', help='display read-only settings as well')
            set_parser.add_argument('-l', '--long', action='store_true', help='describe function of parameter')
            set_parser.add_argument('param', nargs=(argparse.OPTIONAL), help='parameter to set or view', choices_method=_get_settable_completion_items,
              descriptive_header='Description')
            set_parser.add_argument('value', nargs=(argparse.OPTIONAL), help='the new value for settable')

            @with_argparser(set_parser)
            def thgcmd_set(self, args: argparse.Namespace) -> None:
                """Set a settable parameter or show current settings of parameters"""
                if not args.param:
                    return self._show(args)
                    param = utils.norm_fold(args.param.strip())
                    if not args.value:
                        return self._show(args, param)
                else:
                    value = args.value
                    if param not in self.settable:
                        hits = [p for p in self.settable if p.startswith(param)]
                        if len(hits) == 1:
                            param = hits[0]
                        else:
                            return self._show(args, param)
                    orig_value = getattr(self, param)
                    setattr(self, param, utils.cast(orig_value, value))
                    new_value = getattr(self, param)
                    self.poutput('{} - was: {}\nnow: {}'.format(param, orig_value, new_value))
                    if orig_value != new_value:
                        onchange_hook = getattr(self, '_onchange_{}'.format(param), None)
                        if onchange_hook is not None:
                            onchange_hook(old=orig_value, new=new_value)

            shell_parser = ArgParser()
            shell_parser.add_argument('command', help='the command to run', completer_method=shell_cmd_complete)
            shell_parser.add_argument('command_args', nargs=(argparse.REMAINDER), help='arguments to pass to command', completer_method=path_complete)

            @with_argparser(shell_parser, preserve_quotes=True)
            def thgcmd_shell(self, args: argparse.Namespace) -> None:
                """Execute a command as if at the OS prompt"""
                import subprocess
                tokens = [
                 args.command] + args.command_args
                utils.expand_user_in_tokens(tokens)
                expanded_command = ' '.join(tokens)
                with self.sigint_protection:
                    proc = subprocess.Popen(expanded_command, stdout=(subprocess.PIPE if isinstance(self.stdout, utils.StdSim) else self.stdout),
                      stderr=(subprocess.PIPE if isinstance(sys.stderr, utils.StdSim) else sys.stderr),
                      shell=True)
                    proc_reader = utils.ProcReader(proc, self.stdout, sys.stderr)
                    proc_reader.wait()

            @staticmethod
            def _reset_py_display() -> None:
                """
        Resets the dynamic objects in the sys module that the py and ipy consoles fight over.
        When a Python console starts it adopts certain display settings if they've already been set.
        If an ipy console has previously been run, then py uses its settings and ends up looking
        like an ipy console in terms of prompt and exception text. This method forces the Python
        console to create its own display settings since they won't exist.

        IPython does not have this problem since it always overwrites the display settings when it
        is run. Therefore this method only needs to be called before creating a Python console.
        """
                attributes = [
                 'ps1', 'ps2', 'ps3']
                for cur_attr in attributes:
                    try:
                        del sys.__dict__[cur_attr]
                    except KeyError:
                        pass

                sys.displayhook = sys.__displayhook__
                sys.excepthook = sys.__excepthook__

            py_description = "Invoke Python command or shell\n\nNote that, when invoking a command directly from the command line, this shell\nhas limited ability to parse Python statements into tokens. In particular,\nthere may be problems with whitespace and quotes depending on their placement.\n\nIf you see strange parsing behavior, it's best to just open the Python shell\nby providing no arguments to py and run more complex statements there."
            py_parser = ArgParser(description=py_description)
            py_parser.add_argument('command', nargs=(argparse.OPTIONAL), help='command to run')
            py_parser.add_argument('remainder', nargs=(argparse.REMAINDER), help='remainder of command')

            @with_argparser(py_parser, preserve_quotes=True)
            def thgcmd_py--- This code section failed: ---

 L.3040         0  LOAD_CONST               1
                2  LOAD_CONST               ('PyscriptBridge',)
                4  IMPORT_NAME              pyscript_bridge
                6  IMPORT_FROM              PyscriptBridge
                8  STORE_FAST               'PyscriptBridge'
               10  POP_TOP          

 L.3041        12  LOAD_DEREF               'self'
               14  LOAD_ATTR                _in_py
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L.3042        18  LOAD_STR                 'Recursively entering interactive Python consoles is not allowed.'
               20  STORE_FAST               'err'

 L.3043        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              perror
               26  LOAD_FAST                'err'
               28  CALL_METHOD_1         1  '1 positional argument'
               30  POP_TOP          

 L.3044        32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            16  '16'

 L.3046        36  LOAD_FAST                'PyscriptBridge'
               38  LOAD_DEREF               'self'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  STORE_DEREF              'bridge'

 L.3048     44_46  SETUP_FINALLY       954  'to 954'
            48_50  SETUP_EXCEPT        928  'to 928'

 L.3049        52  LOAD_CONST               True
               54  LOAD_DEREF               'self'
               56  STORE_ATTR               _in_py

 L.3052        58  LOAD_GLOBAL              str
               60  LOAD_CONST               ('filename',)
               62  BUILD_CONST_KEY_MAP_1     1 
               64  LOAD_CLOSURE             'bridge'
               66  LOAD_CLOSURE             'interp'
               68  LOAD_CLOSURE             'self'
               70  BUILD_TUPLE_3         3 
               72  LOAD_CODE                <code_object py_run>
               74  LOAD_STR                 'Cmd.thgcmd_py.<locals>.py_run'
               76  MAKE_FUNCTION_12         'annotation, closure'
               78  STORE_FAST               'py_run'

 L.3067        80  LOAD_CODE                <code_object py_quit>
               82  LOAD_STR                 'Cmd.thgcmd_py.<locals>.py_quit'
               84  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               86  STORE_FAST               'py_quit'

 L.3072        88  LOAD_DEREF               'bridge'
               90  LOAD_DEREF               'self'
               92  LOAD_ATTR                _pystate
               94  LOAD_DEREF               'self'
               96  LOAD_ATTR                pyscript_name
               98  STORE_SUBSCR     

 L.3073       100  LOAD_FAST                'py_run'
              102  LOAD_DEREF               'self'
              104  LOAD_ATTR                _pystate
              106  LOAD_STR                 'run'
              108  STORE_SUBSCR     

 L.3074       110  LOAD_FAST                'py_quit'
              112  LOAD_DEREF               'self'
              114  LOAD_ATTR                _pystate
              116  LOAD_STR                 'quit'
              118  STORE_SUBSCR     

 L.3075       120  LOAD_FAST                'py_quit'
              122  LOAD_DEREF               'self'
              124  LOAD_ATTR                _pystate
              126  LOAD_STR                 'exit'
              128  STORE_SUBSCR     

 L.3077       130  LOAD_DEREF               'self'
              132  LOAD_ATTR                locals_in_py
              134  POP_JUMP_IF_FALSE   148  'to 148'

 L.3078       136  LOAD_DEREF               'self'
              138  LOAD_DEREF               'self'
              140  LOAD_ATTR                _pystate
              142  LOAD_STR                 'self'
              144  STORE_SUBSCR     
              146  JUMP_FORWARD        166  'to 166'
            148_0  COME_FROM           134  '134'

 L.3079       148  LOAD_STR                 'self'
              150  LOAD_DEREF               'self'
              152  LOAD_ATTR                _pystate
              154  COMPARE_OP               in
              156  POP_JUMP_IF_FALSE   166  'to 166'

 L.3080       158  LOAD_DEREF               'self'
              160  LOAD_ATTR                _pystate
              162  LOAD_STR                 'self'
              164  DELETE_SUBSCR    
            166_0  COME_FROM           156  '156'
            166_1  COME_FROM           146  '146'

 L.3082       166  LOAD_DEREF               'self'
              168  LOAD_ATTR                _pystate
              170  STORE_FAST               'localvars'

 L.3083       172  LOAD_CONST               0
              174  LOAD_CONST               ('InteractiveConsole',)
              176  IMPORT_NAME              code
              178  IMPORT_FROM              InteractiveConsole
              180  STORE_FAST               'InteractiveConsole'
              182  POP_TOP          

 L.3084       184  LOAD_FAST                'InteractiveConsole'
              186  LOAD_FAST                'localvars'
              188  LOAD_CONST               ('locals',)
              190  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              192  STORE_DEREF              'interp'

 L.3085       194  LOAD_DEREF               'interp'
              196  LOAD_METHOD              runcode
              198  LOAD_STR                 'import sys, os;sys.path.insert(0, os.getcwd())'
              200  CALL_METHOD_1         1  '1 positional argument'
              202  POP_TOP          

 L.3088       204  LOAD_FAST                'args'
              206  LOAD_ATTR                command
          208_210  POP_JUMP_IF_FALSE   292  'to 292'

 L.3089       212  LOAD_FAST                'args'
              214  LOAD_ATTR                command
              216  STORE_FAST               'full_command'

 L.3090       218  LOAD_FAST                'args'
              220  LOAD_ATTR                remainder
              222  POP_JUMP_IF_FALSE   244  'to 244'

 L.3091       224  LOAD_FAST                'full_command'
              226  LOAD_STR                 ' '
              228  LOAD_STR                 ' '
              230  LOAD_METHOD              join
              232  LOAD_FAST                'args'
              234  LOAD_ATTR                remainder
              236  CALL_METHOD_1         1  '1 positional argument'
              238  BINARY_ADD       
              240  INPLACE_ADD      
              242  STORE_FAST               'full_command'
            244_0  COME_FROM           222  '222'

 L.3095       244  LOAD_CONST               True
              246  LOAD_DEREF               'bridge'
              248  STORE_ATTR               cmd_echo

 L.3098       250  SETUP_EXCEPT        266  'to 266'

 L.3099       252  LOAD_DEREF               'interp'
              254  LOAD_METHOD              runcode
              256  LOAD_FAST                'full_command'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  POP_TOP          
              262  POP_BLOCK        
              264  JUMP_FORWARD        924  'to 924'
            266_0  COME_FROM_EXCEPT    250  '250'

 L.3100       266  DUP_TOP          
              268  LOAD_GLOBAL              BaseException
              270  COMPARE_OP               exception-match
          272_274  POP_JUMP_IF_FALSE   286  'to 286'
              276  POP_TOP          
              278  POP_TOP          
              280  POP_TOP          

 L.3102       282  POP_EXCEPT       
              284  JUMP_FORWARD        924  'to 924'
            286_0  COME_FROM           272  '272'
              286  END_FINALLY      
          288_290  JUMP_FORWARD        924  'to 924'
            292_0  COME_FROM           208  '208'

 L.3107       292  LOAD_GLOBAL              rl_type
              294  LOAD_GLOBAL              RlType
              296  LOAD_ATTR                NONE
              298  COMPARE_OP               !=
          300_302  POP_JUMP_IF_FALSE   596  'to 596'

 L.3109       304  BUILD_LIST_0          0 
              306  STORE_FAST               'saved_cmd2_history'

 L.3110       308  SETUP_LOOP          354  'to 354'
              310  LOAD_GLOBAL              range
              312  LOAD_CONST               1
              314  LOAD_GLOBAL              readline
              316  LOAD_METHOD              get_current_history_length
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  LOAD_CONST               1
              322  BINARY_ADD       
              324  CALL_FUNCTION_2       2  '2 positional arguments'
              326  GET_ITER         
              328  FOR_ITER            352  'to 352'
              330  STORE_FAST               'i'

 L.3112       332  LOAD_FAST                'saved_cmd2_history'
              334  LOAD_METHOD              append
              336  LOAD_GLOBAL              readline
              338  LOAD_METHOD              get_history_item
              340  LOAD_FAST                'i'
              342  CALL_METHOD_1         1  '1 positional argument'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  POP_TOP          
          348_350  JUMP_BACK           328  'to 328'
              352  POP_BLOCK        
            354_0  COME_FROM_LOOP      308  '308'

 L.3114       354  LOAD_GLOBAL              readline
              356  LOAD_METHOD              clear_history
              358  CALL_METHOD_0         0  '0 positional arguments'
              360  POP_TOP          

 L.3117       362  SETUP_LOOP          390  'to 390'
              364  LOAD_DEREF               'self'
              366  LOAD_ATTR                _py_history
              368  GET_ITER         
              370  FOR_ITER            388  'to 388'
              372  STORE_FAST               'item'

 L.3118       374  LOAD_GLOBAL              readline
              376  LOAD_METHOD              add_history
              378  LOAD_FAST                'item'
              380  CALL_METHOD_1         1  '1 positional argument'
              382  POP_TOP          
          384_386  JUMP_BACK           370  'to 370'
              388  POP_BLOCK        
            390_0  COME_FROM_LOOP      362  '362'

 L.3120       390  LOAD_DEREF               'self'
              392  LOAD_ATTR                use_rawinput
          394_396  POP_JUMP_IF_FALSE   596  'to 596'
              398  LOAD_DEREF               'self'
              400  LOAD_ATTR                completekey
          402_404  POP_JUMP_IF_FALSE   596  'to 596'

 L.3123       406  LOAD_GLOBAL              rl_type
              408  LOAD_GLOBAL              RlType
              410  LOAD_ATTR                GNU
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   494  'to 494'

 L.3124       418  LOAD_GLOBAL              ctypes
              420  LOAD_METHOD              cast
              422  LOAD_GLOBAL              rl_basic_quote_characters
              424  LOAD_GLOBAL              ctypes
              426  LOAD_ATTR                c_void_p
              428  CALL_METHOD_2         2  '2 positional arguments'
              430  LOAD_ATTR                value
              432  STORE_FAST               'saved_basic_quotes'

 L.3125       434  LOAD_GLOBAL              orig_rl_basic_quotes
              436  LOAD_GLOBAL              rl_basic_quote_characters
              438  STORE_ATTR               value

 L.3127       440  LOAD_STR                 'gnureadline'
              442  LOAD_GLOBAL              sys
              444  LOAD_ATTR                modules
              446  COMPARE_OP               in
          448_450  POP_JUMP_IF_FALSE   494  'to 494'

 L.3130       452  LOAD_CONST               None
              454  STORE_FAST               'saved_readline'

 L.3131       456  LOAD_STR                 'readline'
              458  LOAD_GLOBAL              sys
              460  LOAD_ATTR                modules
              462  COMPARE_OP               in
          464_466  POP_JUMP_IF_FALSE   478  'to 478'

 L.3132       468  LOAD_GLOBAL              sys
              470  LOAD_ATTR                modules
              472  LOAD_STR                 'readline'
              474  BINARY_SUBSCR    
              476  STORE_FAST               'saved_readline'
            478_0  COME_FROM           464  '464'

 L.3134       478  LOAD_GLOBAL              sys
              480  LOAD_ATTR                modules
              482  LOAD_STR                 'gnureadline'
              484  BINARY_SUBSCR    
              486  LOAD_GLOBAL              sys
              488  LOAD_ATTR                modules
              490  LOAD_STR                 'readline'
              492  STORE_SUBSCR     
            494_0  COME_FROM           448  '448'
            494_1  COME_FROM           414  '414'

 L.3136       494  LOAD_GLOBAL              readline
              496  LOAD_METHOD              get_completer_delims
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  STORE_FAST               'saved_delims'

 L.3137       502  LOAD_GLOBAL              readline
              504  LOAD_METHOD              set_completer_delims
              506  LOAD_GLOBAL              orig_rl_delims
              508  CALL_METHOD_1         1  '1 positional argument'
              510  POP_TOP          

 L.3141       512  LOAD_GLOBAL              rl_type
              514  LOAD_GLOBAL              RlType
              516  LOAD_ATTR                GNU
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   536  'to 536'

 L.3142       524  LOAD_GLOBAL              readline
              526  LOAD_METHOD              set_completion_display_matches_hook
              528  LOAD_CONST               None
              530  CALL_METHOD_1         1  '1 positional argument'
              532  POP_TOP          
              534  JUMP_FORWARD        558  'to 558'
            536_0  COME_FROM           520  '520'

 L.3143       536  LOAD_GLOBAL              rl_type
              538  LOAD_GLOBAL              RlType
              540  LOAD_ATTR                PYREADLINE
              542  COMPARE_OP               ==
          544_546  POP_JUMP_IF_FALSE   558  'to 558'

 L.3145       548  LOAD_GLOBAL              orig_pyreadline_display
              550  LOAD_GLOBAL              readline
              552  LOAD_ATTR                rl
              554  LOAD_ATTR                mode
              556  STORE_ATTR               _display_completions
            558_0  COME_FROM           544  '544'
            558_1  COME_FROM           534  '534'

 L.3149       558  LOAD_GLOBAL              readline
              560  LOAD_METHOD              get_completer
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  STORE_FAST               'saved_completer'

 L.3150       566  LOAD_DEREF               'interp'
              568  LOAD_METHOD              runcode
              570  LOAD_STR                 'from rlcompleter import Completer'
              572  CALL_METHOD_1         1  '1 positional argument'
              574  POP_TOP          

 L.3151       576  LOAD_DEREF               'interp'
              578  LOAD_METHOD              runcode
              580  LOAD_STR                 'import readline'
              582  CALL_METHOD_1         1  '1 positional argument'
              584  POP_TOP          

 L.3152       586  LOAD_DEREF               'interp'
              588  LOAD_METHOD              runcode
              590  LOAD_STR                 'readline.set_completer(Completer(locals()).complete)'
              592  CALL_METHOD_1         1  '1 positional argument'
              594  POP_TOP          
            596_0  COME_FROM           402  '402'
            596_1  COME_FROM           394  '394'
            596_2  COME_FROM           300  '300'

 L.3155       596  LOAD_DEREF               'self'
              598  LOAD_METHOD              _reset_py_display
              600  CALL_METHOD_0         0  '0 positional arguments'
              602  POP_TOP          

 L.3157       604  LOAD_GLOBAL              sys
              606  LOAD_ATTR                stdout
              608  STORE_FAST               'saved_sys_stdout'

 L.3158       610  LOAD_DEREF               'self'
              612  LOAD_ATTR                stdout
              614  LOAD_GLOBAL              sys
              616  STORE_ATTR               stdout

 L.3160       618  LOAD_GLOBAL              sys
              620  LOAD_ATTR                stdin
              622  STORE_FAST               'saved_sys_stdin'

 L.3161       624  LOAD_DEREF               'self'
              626  LOAD_ATTR                stdin
              628  LOAD_GLOBAL              sys
              630  STORE_ATTR               stdin

 L.3163       632  LOAD_STR                 'Type "help", "copyright", "credits" or "license" for more information.'
              634  STORE_FAST               'cprt'

 L.3164       636  LOAD_STR                 'End with `Ctrl-D` (Unix) / `Ctrl-Z` (Windows), `quit()`, `exit()`.\nNon-Python commands can be issued with: {}("your command")\nRun Python code from external script files with: run("script.py")'
              638  LOAD_METHOD              format

 L.3167       640  LOAD_DEREF               'self'
              642  LOAD_ATTR                pyscript_name
              644  CALL_METHOD_1         1  '1 positional argument'
              646  STORE_FAST               'instructions'

 L.3170       648  SETUP_FINALLY       710  'to 710'
              650  SETUP_EXCEPT        684  'to 684'

 L.3171       652  LOAD_DEREF               'interp'
              654  LOAD_ATTR                interact
              656  LOAD_STR                 'Python {} on {}\n{}\n\n{}\n'
              658  LOAD_METHOD              format

 L.3172       660  LOAD_GLOBAL              sys
              662  LOAD_ATTR                version
              664  LOAD_GLOBAL              sys
              666  LOAD_ATTR                platform
              668  LOAD_FAST                'cprt'
              670  LOAD_FAST                'instructions'
              672  CALL_METHOD_4         4  '4 positional arguments'
              674  LOAD_CONST               ('banner',)
              676  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              678  POP_TOP          
              680  POP_BLOCK        
              682  JUMP_FORWARD        706  'to 706'
            684_0  COME_FROM_EXCEPT    650  '650'

 L.3173       684  DUP_TOP          
              686  LOAD_GLOBAL              BaseException
              688  COMPARE_OP               exception-match
          690_692  POP_JUMP_IF_FALSE   704  'to 704'
              694  POP_TOP          
              696  POP_TOP          
              698  POP_TOP          

 L.3175       700  POP_EXCEPT       
              702  JUMP_FORWARD        706  'to 706'
            704_0  COME_FROM           690  '690'
              704  END_FINALLY      
            706_0  COME_FROM           702  '702'
            706_1  COME_FROM           682  '682'
              706  POP_BLOCK        
              708  LOAD_CONST               None
            710_0  COME_FROM_FINALLY   648  '648'

 L.3178       710  LOAD_FAST                'saved_sys_stdout'
              712  LOAD_GLOBAL              sys
              714  STORE_ATTR               stdout

 L.3179       716  LOAD_FAST                'saved_sys_stdin'
              718  LOAD_GLOBAL              sys
              720  STORE_ATTR               stdin

 L.3182       722  LOAD_GLOBAL              rl_type
              724  LOAD_GLOBAL              RlType
              726  LOAD_ATTR                NONE
              728  COMPARE_OP               !=
          730_732  POP_JUMP_IF_FALSE   922  'to 922'

 L.3184       734  LOAD_DEREF               'self'
              736  LOAD_ATTR                _py_history
              738  LOAD_METHOD              clear
              740  CALL_METHOD_0         0  '0 positional arguments'
              742  POP_TOP          

 L.3185       744  SETUP_LOOP          792  'to 792'
              746  LOAD_GLOBAL              range
              748  LOAD_CONST               1
              750  LOAD_GLOBAL              readline
              752  LOAD_METHOD              get_current_history_length
              754  CALL_METHOD_0         0  '0 positional arguments'
              756  LOAD_CONST               1
              758  BINARY_ADD       
              760  CALL_FUNCTION_2       2  '2 positional arguments'
              762  GET_ITER         
              764  FOR_ITER            790  'to 790'
              766  STORE_FAST               'i'

 L.3187       768  LOAD_DEREF               'self'
              770  LOAD_ATTR                _py_history
              772  LOAD_METHOD              append
              774  LOAD_GLOBAL              readline
              776  LOAD_METHOD              get_history_item
              778  LOAD_FAST                'i'
              780  CALL_METHOD_1         1  '1 positional argument'
              782  CALL_METHOD_1         1  '1 positional argument'
              784  POP_TOP          
          786_788  JUMP_BACK           764  'to 764'
              790  POP_BLOCK        
            792_0  COME_FROM_LOOP      744  '744'

 L.3189       792  LOAD_GLOBAL              readline
              794  LOAD_METHOD              clear_history
              796  CALL_METHOD_0         0  '0 positional arguments'
              798  POP_TOP          

 L.3192       800  SETUP_LOOP          826  'to 826'
              802  LOAD_FAST                'saved_cmd2_history'
              804  GET_ITER         
              806  FOR_ITER            824  'to 824'
              808  STORE_FAST               'item'

 L.3193       810  LOAD_GLOBAL              readline
              812  LOAD_METHOD              add_history
              814  LOAD_FAST                'item'
              816  CALL_METHOD_1         1  '1 positional argument'
              818  POP_TOP          
          820_822  JUMP_BACK           806  'to 806'
              824  POP_BLOCK        
            826_0  COME_FROM_LOOP      800  '800'

 L.3195       826  LOAD_DEREF               'self'
              828  LOAD_ATTR                use_rawinput
          830_832  POP_JUMP_IF_FALSE   922  'to 922'
              834  LOAD_DEREF               'self'
              836  LOAD_ATTR                completekey
          838_840  POP_JUMP_IF_FALSE   922  'to 922'

 L.3197       842  LOAD_GLOBAL              readline
              844  LOAD_METHOD              set_completer
              846  LOAD_FAST                'saved_completer'
              848  CALL_METHOD_1         1  '1 positional argument'
              850  POP_TOP          

 L.3198       852  LOAD_GLOBAL              readline
              854  LOAD_METHOD              set_completer_delims
              856  LOAD_FAST                'saved_delims'
              858  CALL_METHOD_1         1  '1 positional argument'
              860  POP_TOP          

 L.3200       862  LOAD_GLOBAL              rl_type
              864  LOAD_GLOBAL              RlType
              866  LOAD_ATTR                GNU
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   922  'to 922'

 L.3201       874  LOAD_FAST                'saved_basic_quotes'
              876  LOAD_GLOBAL              rl_basic_quote_characters
              878  STORE_ATTR               value

 L.3203       880  LOAD_STR                 'gnureadline'
              882  LOAD_GLOBAL              sys
              884  LOAD_ATTR                modules
              886  COMPARE_OP               in
          888_890  POP_JUMP_IF_FALSE   922  'to 922'

 L.3205       892  LOAD_FAST                'saved_readline'
              894  LOAD_CONST               None
              896  COMPARE_OP               is
            898_0  COME_FROM           264  '264'
          898_900  POP_JUMP_IF_FALSE   912  'to 912'

 L.3206       902  LOAD_GLOBAL              sys
              904  LOAD_ATTR                modules
              906  LOAD_STR                 'readline'
              908  DELETE_SUBSCR    
              910  JUMP_FORWARD        922  'to 922'
            912_0  COME_FROM           898  '898'

 L.3208       912  LOAD_FAST                'saved_readline'
              914  LOAD_GLOBAL              sys
              916  LOAD_ATTR                modules
            918_0  COME_FROM           284  '284'
              918  LOAD_STR                 'readline'
              920  STORE_SUBSCR     
            922_0  COME_FROM           910  '910'
            922_1  COME_FROM           888  '888'
            922_2  COME_FROM           870  '870'
            922_3  COME_FROM           838  '838'
            922_4  COME_FROM           830  '830'
            922_5  COME_FROM           730  '730'
              922  END_FINALLY      
            924_0  COME_FROM           288  '288'
              924  POP_BLOCK        
              926  JUMP_FORWARD        950  'to 950'
            928_0  COME_FROM_EXCEPT     48  '48'

 L.3210       928  DUP_TOP          
              930  LOAD_GLOBAL              KeyboardInterrupt
              932  COMPARE_OP               exception-match
          934_936  POP_JUMP_IF_FALSE   948  'to 948'
              938  POP_TOP          
              940  POP_TOP          
              942  POP_TOP          

 L.3211       944  POP_EXCEPT       
              946  JUMP_FORWARD        950  'to 950'
            948_0  COME_FROM           934  '934'
              948  END_FINALLY      
            950_0  COME_FROM           946  '946'
            950_1  COME_FROM           926  '926'
              950  POP_BLOCK        
              952  LOAD_CONST               None
            954_0  COME_FROM_FINALLY    44  '44'

 L.3214       954  LOAD_CONST               False
              956  LOAD_DEREF               'self'
              958  STORE_ATTR               _in_py
              960  END_FINALLY      

 L.3216       962  LOAD_DEREF               'bridge'
              964  LOAD_ATTR                stop
              966  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 898_900

            run_pyscript_parser = ArgParser()
            run_pyscript_parser.add_argument('script_path', help='path to the script file', completer_method=path_complete)
            run_pyscript_parser.add_argument('script_arguments', nargs=(argparse.REMAINDER), help='arguments to pass to script',
              completer_method=path_complete)

            @with_argparser(run_pyscript_parser)
            def thgcmd_run_pyscript(self, args: argparse.Namespace) -> bool:
                """Run a Python script file inside the console"""
                script_path = os.path.expanduser(args.script_path)
                py_return = False
                orig_args = sys.argv
                try:
                    try:
                        sys.argv = [
                         script_path] + args.script_arguments
                        py_return = self.thgcmd_py('run({!r})'.format(script_path))
                    except KeyboardInterrupt:
                        pass

                finally:
                    sys.argv = orig_args

                return py_return

            if ipython_available:

                @with_argparser(ArgParser())
                def thgcmd_ipy(self, _: argparse.Namespace) -> None:
                    """Enter an interactive IPython shell"""
                    from .pyscript_bridge import PyscriptBridge
                    bridge = PyscriptBridge(self)
                    banner = 'Entering an embedded IPython shell. Type quit or <Ctrl>-d to exit.\nRun Python code from external files with: run filename.py\n'
                    exit_msg = 'Leaving IPython, back to {}'.format(sys.argv[0])
                    if self.locals_in_py:

                        def load_ipy(cmd2_instance, app):
                            embed(banner1=banner, exit_msg=exit_msg)

                        load_ipy(self, bridge)
                    else:

                        def load_ipy(app):
                            embed(banner1=banner, exit_msg=exit_msg)

                        load_ipy(bridge)

            history_description = 'View, run, edit, save, or clear previously entered commands'
            history_parser = ArgParser(description=history_description)
            history_action_group = history_parser.add_mutually_exclusive_group()
            history_action_group.add_argument('-r', '--run', action='store_true', help='run selected history items')
            history_action_group.add_argument('-e', '--edit', action='store_true', help='edit and then run selected history items')
            history_action_group.add_argument('-o', '--output_file', metavar='FILE', help='output commands to a script file, implies -s',
              completer_method=path_complete)
            history_action_group.add_argument('-t', '--transcript', metavar='TRANSCRIPT_FILE', help='output commands and results to a transcript file,\nimplies -s',
              completer_method=path_complete)
            history_action_group.add_argument('-c', '--clear', action='store_true', help='clear all history')
            history_format_group = history_parser.add_argument_group(title='formatting')
            history_format_group.add_argument('-s', '--script', action='store_true', help='output commands in script format, i.e. without command\nnumbers')
            history_format_group.add_argument('-x', '--expanded', action='store_true', help='output fully parsed commands with any aliases and\nmacros expanded, instead of typed commands')
            history_format_group.add_argument('-v', '--verbose', action='store_true', help='display history and include expanded commands if they\ndiffer from the typed command')
            history_format_group.add_argument('-a', '--all', action='store_true', help='display all commands, including ones persisted from\nprevious sessions')
            history_arg_help = 'empty               all history items\na                   one history item by number\na..b, a:b, a:, ..b  items by indices (inclusive)\nstring              items containing string\n/regex/             items matching regular expression'
            history_parser.add_argument('arg', nargs=(argparse.OPTIONAL), help=history_arg_help)

            @with_argparser(history_parser)
            def thgcmd_history--- This code section failed: ---

 L.3316         0  LOAD_FAST                'args'
                2  LOAD_ATTR                verbose
                4  POP_JUMP_IF_FALSE    78  'to 78'

 L.3317         6  LOAD_FAST                'args'
                8  LOAD_ATTR                clear
               10  POP_JUMP_IF_TRUE     48  'to 48'
               12  LOAD_FAST                'args'
               14  LOAD_ATTR                edit
               16  POP_JUMP_IF_TRUE     48  'to 48'
               18  LOAD_FAST                'args'
               20  LOAD_ATTR                output_file
               22  POP_JUMP_IF_TRUE     48  'to 48'
               24  LOAD_FAST                'args'
               26  LOAD_ATTR                run
               28  POP_JUMP_IF_TRUE     48  'to 48'
               30  LOAD_FAST                'args'
               32  LOAD_ATTR                transcript
               34  POP_JUMP_IF_TRUE     48  'to 48'

 L.3318        36  LOAD_FAST                'args'
               38  LOAD_ATTR                expanded
               40  POP_JUMP_IF_TRUE     48  'to 48'
               42  LOAD_FAST                'args'
               44  LOAD_ATTR                script
               46  POP_JUMP_IF_FALSE    78  'to 78'
             48_0  COME_FROM            40  '40'
             48_1  COME_FROM            34  '34'
             48_2  COME_FROM            28  '28'
             48_3  COME_FROM            22  '22'
             48_4  COME_FROM            16  '16'
             48_5  COME_FROM            10  '10'

 L.3319        48  LOAD_FAST                'self'
               50  LOAD_METHOD              poutput
               52  LOAD_STR                 '-v can not be used with any other options'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  POP_TOP          

 L.3320        58  LOAD_FAST                'self'
               60  LOAD_METHOD              poutput
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                history_parser
               66  LOAD_METHOD              format_usage
               68  CALL_METHOD_0         0  '0 positional arguments'
               70  CALL_METHOD_1         1  '1 positional argument'
               72  POP_TOP          

 L.3321        74  LOAD_CONST               None
               76  RETURN_VALUE     
             78_0  COME_FROM            46  '46'
             78_1  COME_FROM             4  '4'

 L.3324        78  LOAD_FAST                'args'
               80  LOAD_ATTR                script
               82  POP_JUMP_IF_TRUE     90  'to 90'
               84  LOAD_FAST                'args'
               86  LOAD_ATTR                expanded
               88  POP_JUMP_IF_FALSE   150  'to 150'
             90_0  COME_FROM            82  '82'

 L.3325        90  LOAD_FAST                'args'
               92  LOAD_ATTR                clear
               94  POP_JUMP_IF_TRUE    120  'to 120'
               96  LOAD_FAST                'args'
               98  LOAD_ATTR                edit
              100  POP_JUMP_IF_TRUE    120  'to 120'
              102  LOAD_FAST                'args'
              104  LOAD_ATTR                output_file
              106  POP_JUMP_IF_TRUE    120  'to 120'
              108  LOAD_FAST                'args'
              110  LOAD_ATTR                run
              112  POP_JUMP_IF_TRUE    120  'to 120'
              114  LOAD_FAST                'args'
              116  LOAD_ATTR                transcript
              118  POP_JUMP_IF_FALSE   150  'to 150'
            120_0  COME_FROM           112  '112'
            120_1  COME_FROM           106  '106'
            120_2  COME_FROM           100  '100'
            120_3  COME_FROM            94  '94'

 L.3326       120  LOAD_FAST                'self'
              122  LOAD_METHOD              poutput
              124  LOAD_STR                 '-s and -x can not be used with -c, -r, -e, -o, or -t'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  POP_TOP          

 L.3327       130  LOAD_FAST                'self'
              132  LOAD_METHOD              poutput
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                history_parser
              138  LOAD_METHOD              format_usage
              140  CALL_METHOD_0         0  '0 positional arguments'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  POP_TOP          

 L.3328       146  LOAD_CONST               None
              148  RETURN_VALUE     
            150_0  COME_FROM           118  '118'
            150_1  COME_FROM            88  '88'

 L.3330       150  LOAD_FAST                'args'
              152  LOAD_ATTR                clear
              154  POP_JUMP_IF_FALSE   206  'to 206'

 L.3332       156  LOAD_FAST                'self'
              158  LOAD_ATTR                history
              160  LOAD_METHOD              clear
              162  CALL_METHOD_0         0  '0 positional arguments'
              164  POP_TOP          

 L.3334       166  LOAD_FAST                'self'
              168  LOAD_ATTR                persistent_history_file
              170  POP_JUMP_IF_FALSE   184  'to 184'

 L.3335       172  LOAD_GLOBAL              os
              174  LOAD_METHOD              remove
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                persistent_history_file
              180  CALL_METHOD_1         1  '1 positional argument'
              182  POP_TOP          
            184_0  COME_FROM           170  '170'

 L.3337       184  LOAD_GLOBAL              rl_type
              186  LOAD_GLOBAL              RlType
              188  LOAD_ATTR                NONE
              190  COMPARE_OP               !=
              192  POP_JUMP_IF_FALSE   202  'to 202'

 L.3338       194  LOAD_GLOBAL              readline
              196  LOAD_METHOD              clear_history
              198  CALL_METHOD_0         0  '0 positional arguments'
              200  POP_TOP          
            202_0  COME_FROM           192  '192'

 L.3339       202  LOAD_CONST               None
              204  RETURN_VALUE     
            206_0  COME_FROM           154  '154'

 L.3342       206  LOAD_CONST               False
              208  STORE_FAST               'cowardly_refuse_to_run'

 L.3343       210  LOAD_FAST                'args'
              212  LOAD_ATTR                arg
          214_216  POP_JUMP_IF_FALSE   388  'to 388'

 L.3346       218  LOAD_FAST                'args'
              220  LOAD_ATTR                arg
              222  STORE_FAST               'arg'

 L.3347       224  LOAD_CONST               False
              226  STORE_FAST               'arg_is_int'

 L.3348       228  SETUP_EXCEPT        246  'to 246'

 L.3349       230  LOAD_GLOBAL              int
              232  LOAD_FAST                'arg'
              234  CALL_FUNCTION_1       1  '1 positional argument'
              236  POP_TOP          

 L.3350       238  LOAD_CONST               True
              240  STORE_FAST               'arg_is_int'
              242  POP_BLOCK        
              244  JUMP_FORWARD        268  'to 268'
            246_0  COME_FROM_EXCEPT    228  '228'

 L.3351       246  DUP_TOP          
              248  LOAD_GLOBAL              ValueError
              250  COMPARE_OP               exception-match
          252_254  POP_JUMP_IF_FALSE   266  'to 266'
              256  POP_TOP          
              258  POP_TOP          
              260  POP_TOP          

 L.3352       262  POP_EXCEPT       
              264  JUMP_FORWARD        268  'to 268'
            266_0  COME_FROM           252  '252'
              266  END_FINALLY      
            268_0  COME_FROM           264  '264'
            268_1  COME_FROM           244  '244'

 L.3354       268  LOAD_STR                 '..'
              270  LOAD_FAST                'arg'
              272  COMPARE_OP               in
          274_276  POP_JUMP_IF_TRUE    288  'to 288'
              278  LOAD_STR                 ':'
              280  LOAD_FAST                'arg'
              282  COMPARE_OP               in
          284_286  POP_JUMP_IF_FALSE   306  'to 306'
            288_0  COME_FROM           274  '274'

 L.3356       288  LOAD_FAST                'self'
              290  LOAD_ATTR                history
              292  LOAD_METHOD              span
              294  LOAD_FAST                'arg'
              296  LOAD_FAST                'args'
              298  LOAD_ATTR                all
              300  CALL_METHOD_2         2  '2 positional arguments'
              302  STORE_FAST               'history'
              304  JUMP_FORWARD        386  'to 386'
            306_0  COME_FROM           284  '284'

 L.3357       306  LOAD_FAST                'arg_is_int'
          308_310  POP_JUMP_IF_FALSE   328  'to 328'

 L.3358       312  LOAD_FAST                'self'
              314  LOAD_ATTR                history
              316  LOAD_METHOD              get
              318  LOAD_FAST                'arg'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  BUILD_LIST_1          1 
              324  STORE_FAST               'history'
              326  JUMP_FORWARD        386  'to 386'
            328_0  COME_FROM           308  '308'

 L.3359       328  LOAD_FAST                'arg'
              330  LOAD_METHOD              startswith
              332  LOAD_STR                 '/'
              334  CALL_METHOD_1         1  '1 positional argument'
          336_338  POP_JUMP_IF_FALSE   370  'to 370'
              340  LOAD_FAST                'arg'
              342  LOAD_METHOD              endswith
              344  LOAD_STR                 '/'
              346  CALL_METHOD_1         1  '1 positional argument'
          348_350  POP_JUMP_IF_FALSE   370  'to 370'

 L.3360       352  LOAD_FAST                'self'
              354  LOAD_ATTR                history
              356  LOAD_METHOD              regex_search
              358  LOAD_FAST                'arg'
              360  LOAD_FAST                'args'
              362  LOAD_ATTR                all
              364  CALL_METHOD_2         2  '2 positional arguments'
              366  STORE_FAST               'history'
              368  JUMP_FORWARD        386  'to 386'
            370_0  COME_FROM           348  '348'
            370_1  COME_FROM           336  '336'

 L.3362       370  LOAD_FAST                'self'
              372  LOAD_ATTR                history
              374  LOAD_METHOD              str_search
              376  LOAD_FAST                'arg'
              378  LOAD_FAST                'args'
              380  LOAD_ATTR                all
              382  CALL_METHOD_2         2  '2 positional arguments'
              384  STORE_FAST               'history'
            386_0  COME_FROM           368  '368'
            386_1  COME_FROM           326  '326'
            386_2  COME_FROM           304  '304'
              386  JUMP_FORWARD        408  'to 408'
            388_0  COME_FROM           214  '214'

 L.3365       388  LOAD_CONST               True
              390  STORE_FAST               'cowardly_refuse_to_run'

 L.3367       392  LOAD_FAST                'self'
              394  LOAD_ATTR                history
              396  LOAD_METHOD              span
              398  LOAD_STR                 ':'
              400  LOAD_FAST                'args'
              402  LOAD_ATTR                all
              404  CALL_METHOD_2         2  '2 positional arguments'
              406  STORE_FAST               'history'
            408_0  COME_FROM           386  '386'

 L.3369       408  LOAD_FAST                'args'
              410  LOAD_ATTR                run
          412_414  POP_JUMP_IF_FALSE   458  'to 458'

 L.3370       416  LOAD_FAST                'cowardly_refuse_to_run'
          418_420  POP_JUMP_IF_FALSE   444  'to 444'

 L.3371       422  LOAD_FAST                'self'
              424  LOAD_METHOD              perror
              426  LOAD_STR                 'Cowardly refusing to run all previously entered commands.'
              428  CALL_METHOD_1         1  '1 positional argument'
              430  POP_TOP          

 L.3372       432  LOAD_FAST                'self'
              434  LOAD_METHOD              perror
              436  LOAD_STR                 "If this is what you want to do, specify '1:' as the range of history."
              438  CALL_METHOD_1         1  '1 positional argument'
              440  POP_TOP          
              442  JUMP_FORWARD        910  'to 910'
            444_0  COME_FROM           418  '418'

 L.3374       444  LOAD_FAST                'self'
              446  LOAD_METHOD              runcmds_plus_hooks
              448  LOAD_FAST                'history'
              450  CALL_METHOD_1         1  '1 positional argument'
              452  RETURN_VALUE     
          454_456  JUMP_FORWARD        910  'to 910'
            458_0  COME_FROM           412  '412'

 L.3375       458  LOAD_FAST                'args'
              460  LOAD_ATTR                edit
          462_464  POP_JUMP_IF_FALSE   622  'to 622'

 L.3376       466  LOAD_CONST               0
              468  LOAD_CONST               None
              470  IMPORT_NAME              tempfile
              472  STORE_FAST               'tempfile'

 L.3377       474  LOAD_FAST                'tempfile'
              476  LOAD_ATTR                mkstemp
              478  LOAD_STR                 '.txt'
              480  LOAD_CONST               True
              482  LOAD_CONST               ('suffix', 'text')
              484  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              486  UNPACK_SEQUENCE_2     2 
              488  STORE_FAST               'fd'
              490  STORE_FAST               'fname'

 L.3378       492  LOAD_GLOBAL              os
              494  LOAD_METHOD              fdopen
              496  LOAD_FAST                'fd'
              498  LOAD_STR                 'w'
              500  CALL_METHOD_2         2  '2 positional arguments'
              502  SETUP_WITH          578  'to 578'
              504  STORE_FAST               'fobj'

 L.3379       506  SETUP_LOOP          574  'to 574'
              508  LOAD_FAST                'history'
              510  GET_ITER         
              512  FOR_ITER            572  'to 572'
              514  STORE_FAST               'command'

 L.3380       516  LOAD_FAST                'command'
              518  LOAD_ATTR                statement
              520  LOAD_ATTR                multiline_command
          522_524  POP_JUMP_IF_FALSE   550  'to 550'

 L.3381       526  LOAD_FAST                'fobj'
              528  LOAD_METHOD              write
              530  LOAD_STR                 '{}\n'
              532  LOAD_METHOD              format
              534  LOAD_FAST                'command'
              536  LOAD_ATTR                expanded
              538  LOAD_METHOD              rstrip
              540  CALL_METHOD_0         0  '0 positional arguments'
              542  CALL_METHOD_1         1  '1 positional argument'
              544  CALL_METHOD_1         1  '1 positional argument'
              546  POP_TOP          
              548  JUMP_BACK           512  'to 512'
            550_0  COME_FROM           522  '522'

 L.3383       550  LOAD_FAST                'fobj'
              552  LOAD_METHOD              write
              554  LOAD_STR                 '{}\n'
              556  LOAD_METHOD              format
              558  LOAD_FAST                'command'
              560  LOAD_ATTR                raw
              562  CALL_METHOD_1         1  '1 positional argument'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  POP_TOP          
          568_570  JUMP_BACK           512  'to 512'
              572  POP_BLOCK        
            574_0  COME_FROM_LOOP      506  '506'
              574  POP_BLOCK        
              576  LOAD_CONST               None
            578_0  COME_FROM_WITH      502  '502'
              578  WITH_CLEANUP_START
              580  WITH_CLEANUP_FINISH
              582  END_FINALLY      

 L.3384       584  SETUP_FINALLY       606  'to 606'

 L.3385       586  LOAD_FAST                'self'
              588  LOAD_METHOD              thgcmd_edit
              590  LOAD_FAST                'fname'
              592  CALL_METHOD_1         1  '1 positional argument'
              594  POP_TOP          

 L.3386       596  LOAD_FAST                'self'
              598  LOAD_METHOD              thgcmd_run_script
              600  LOAD_FAST                'fname'
              602  CALL_METHOD_1         1  '1 positional argument'
              604  RETURN_VALUE     
            606_0  COME_FROM_FINALLY   584  '584'

 L.3388       606  LOAD_GLOBAL              os
              608  LOAD_METHOD              remove
              610  LOAD_FAST                'fname'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  POP_TOP          
              616  END_FINALLY      
          618_620  JUMP_FORWARD        910  'to 910'
            622_0  COME_FROM           462  '462'

 L.3389       622  LOAD_FAST                'args'
              624  LOAD_ATTR                output_file
          626_628  POP_JUMP_IF_FALSE   842  'to 842'

 L.3390       630  SETUP_EXCEPT        758  'to 758'

 L.3391       632  LOAD_GLOBAL              open
              634  LOAD_GLOBAL              os
              636  LOAD_ATTR                path
              638  LOAD_METHOD              expanduser
              640  LOAD_FAST                'args'
              642  LOAD_ATTR                output_file
              644  CALL_METHOD_1         1  '1 positional argument'
              646  LOAD_STR                 'w'
              648  CALL_FUNCTION_2       2  '2 positional arguments'
              650  SETUP_WITH          726  'to 726'
              652  STORE_FAST               'fobj'

 L.3392       654  SETUP_LOOP          722  'to 722'
              656  LOAD_FAST                'history'
              658  GET_ITER         
              660  FOR_ITER            720  'to 720'
              662  STORE_FAST               'item'

 L.3393       664  LOAD_FAST                'item'
              666  LOAD_ATTR                statement
              668  LOAD_ATTR                multiline_command
          670_672  POP_JUMP_IF_FALSE   698  'to 698'

 L.3394       674  LOAD_FAST                'fobj'
              676  LOAD_METHOD              write
              678  LOAD_STR                 '{}\n'
              680  LOAD_METHOD              format
              682  LOAD_FAST                'item'
              684  LOAD_ATTR                expanded
              686  LOAD_METHOD              rstrip
              688  CALL_METHOD_0         0  '0 positional arguments'
              690  CALL_METHOD_1         1  '1 positional argument'
              692  CALL_METHOD_1         1  '1 positional argument'
              694  POP_TOP          
              696  JUMP_BACK           660  'to 660'
            698_0  COME_FROM           670  '670'

 L.3396       698  LOAD_FAST                'fobj'
              700  LOAD_METHOD              write
              702  LOAD_STR                 '{}\n'
              704  LOAD_METHOD              format
              706  LOAD_FAST                'item'
              708  LOAD_ATTR                raw
              710  CALL_METHOD_1         1  '1 positional argument'
              712  CALL_METHOD_1         1  '1 positional argument'
              714  POP_TOP          
          716_718  JUMP_BACK           660  'to 660'
              720  POP_BLOCK        
            722_0  COME_FROM_LOOP      654  '654'
              722  POP_BLOCK        
              724  LOAD_CONST               None
            726_0  COME_FROM_WITH      650  '650'
              726  WITH_CLEANUP_START
              728  WITH_CLEANUP_FINISH
              730  END_FINALLY      

 L.3397       732  LOAD_GLOBAL              len
              734  LOAD_FAST                'history'
              736  CALL_FUNCTION_1       1  '1 positional argument'
              738  LOAD_CONST               1
              740  COMPARE_OP               >
          742_744  POP_JUMP_IF_FALSE   750  'to 750'
              746  LOAD_STR                 's'
              748  JUMP_FORWARD        752  'to 752'
            750_0  COME_FROM           742  '742'
              750  LOAD_STR                 ''
            752_0  COME_FROM           748  '748'
              752  STORE_FAST               'plural'
              754  POP_BLOCK        
              756  JUMP_FORWARD        814  'to 814'
            758_0  COME_FROM_EXCEPT    630  '630'

 L.3398       758  DUP_TOP          
              760  LOAD_GLOBAL              OSError
              762  COMPARE_OP               exception-match
          764_766  POP_JUMP_IF_FALSE   812  'to 812'
              768  POP_TOP          
              770  STORE_FAST               'e'
              772  POP_TOP          
              774  SETUP_FINALLY       800  'to 800'

 L.3399       776  LOAD_FAST                'self'
              778  LOAD_METHOD              pexcept
              780  LOAD_STR                 'Error saving {!r} - {}'
              782  LOAD_METHOD              format
              784  LOAD_FAST                'args'
              786  LOAD_ATTR                output_file
              788  LOAD_FAST                'e'
              790  CALL_METHOD_2         2  '2 positional arguments'
              792  CALL_METHOD_1         1  '1 positional argument'
              794  POP_TOP          
              796  POP_BLOCK        
              798  LOAD_CONST               None
            800_0  COME_FROM_FINALLY   774  '774'
              800  LOAD_CONST               None
              802  STORE_FAST               'e'
              804  DELETE_FAST              'e'
              806  END_FINALLY      
              808  POP_EXCEPT       
              810  JUMP_FORWARD        840  'to 840'
            812_0  COME_FROM           764  '764'
              812  END_FINALLY      
            814_0  COME_FROM           756  '756'

 L.3401       814  LOAD_FAST                'self'
              816  LOAD_METHOD              pfeedback
              818  LOAD_STR                 '{} command{} saved to {}'
              820  LOAD_METHOD              format
              822  LOAD_GLOBAL              len
              824  LOAD_FAST                'history'
              826  CALL_FUNCTION_1       1  '1 positional argument'
              828  LOAD_FAST                'plural'
              830  LOAD_FAST                'args'
              832  LOAD_ATTR                output_file
              834  CALL_METHOD_3         3  '3 positional arguments'
              836  CALL_METHOD_1         1  '1 positional argument'
              838  POP_TOP          
            840_0  COME_FROM           810  '810'
              840  JUMP_FORWARD        910  'to 910'
            842_0  COME_FROM           626  '626'

 L.3402       842  LOAD_FAST                'args'
              844  LOAD_ATTR                transcript
          846_848  POP_JUMP_IF_FALSE   866  'to 866'

 L.3403       850  LOAD_FAST                'self'
              852  LOAD_METHOD              _generate_transcript
              854  LOAD_FAST                'history'
              856  LOAD_FAST                'args'
              858  LOAD_ATTR                transcript
              860  CALL_METHOD_2         2  '2 positional arguments'
              862  POP_TOP          
              864  JUMP_FORWARD        910  'to 910'
            866_0  COME_FROM           846  '846'

 L.3406       866  SETUP_LOOP          910  'to 910'
              868  LOAD_FAST                'history'
              870  GET_ITER         
              872  FOR_ITER            908  'to 908'
              874  STORE_FAST               'hi'

 L.3407       876  LOAD_FAST                'self'
              878  LOAD_METHOD              poutput
              880  LOAD_FAST                'hi'
              882  LOAD_ATTR                pr
              884  LOAD_FAST                'args'
              886  LOAD_ATTR                script
              888  LOAD_FAST                'args'
              890  LOAD_ATTR                expanded
              892  LOAD_FAST                'args'
              894  LOAD_ATTR                verbose
            896_0  COME_FROM           442  '442'
              896  LOAD_CONST               ('script', 'expanded', 'verbose')
              898  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              900  CALL_METHOD_1         1  '1 positional argument'
              902  POP_TOP          
          904_906  JUMP_BACK           872  'to 872'
              908  POP_BLOCK        
            910_0  COME_FROM_LOOP      866  '866'
            910_1  COME_FROM           864  '864'
            910_2  COME_FROM           840  '840'
            910_3  COME_FROM           618  '618'
            910_4  COME_FROM           454  '454'

Parse error at or near `COME_FROM' instruction at offset 78_1

            def _initialize_history(self, hist_file):
                """Initialize history using history related attributes

        This function can determine whether history is saved in the prior text-based
        format (one line of input is stored as one line in the file), or the new-as-
        of-version 0.9.13 pickle based format.

        History created by versions <= 0.9.12 is in readline format, i.e. plain text files.

        Initializing history does not effect history files on disk, versions >= 0.9.13 always
        write history in the pickle format.
        """
                self.history = History()
                if not hist_file:
                    self.persistent_history_file = hist_file
                    return
                hist_file = os.path.abspath(os.path.expanduser(hist_file))
                history = History()
                if os.path.isdir(hist_file):
                    msg = "persistent history file '{}' is a directory"
                    self.perror(msg.format(hist_file))
                    return
                try:
                    with open(hist_file, 'rb') as (fobj):
                        history = pickle.load(fobj)
                except (AttributeError, EOFError, FileNotFoundError, ImportError, IndexError, KeyError, pickle.UnpicklingError):
                    pass
                except OSError as ex:
                    try:
                        msg = "can not read persistent history file '{}': {}"
                        self.pexcept(msg.format(hist_file, ex))
                        return
                    finally:
                        ex = None
                        del ex

                self.history = history
                self.history.start_session()
                self.persistent_history_file = hist_file
                if rl_type != RlType.NONE:
                    last = None
                    for item in history:
                        for line in item.raw.splitlines():
                            if line != last:
                                readline.add_history(line)
                                last = line

                import atexit
                atexit.register(self._persist_history)

            def _persist_history(self):
                """write history out to the history file"""
                if not self.persistent_history_file:
                    return
                self.history.truncate(self._persistent_history_length)
                try:
                    with open(self.persistent_history_file, 'wb') as (fobj):
                        pickle.dump(self.history, fobj)
                except OSError as ex:
                    try:
                        msg = "can not write persistent history file '{}': {}"
                        self.pexcept(msg.format(self.persistent_history_file, ex))
                    finally:
                        ex = None
                        del ex

            def _generate_transcript(self, history: List[Union[(HistoryItem, str)]], transcript_file: str) -> None:
                """
        Generate a transcript file from a given history of commands
        """
                transcript_path = os.path.abspath(os.path.expanduser(transcript_file))
                transcript_dir = os.path.dirname(transcript_path)
                if not (os.path.isdir(transcript_dir) and os.access(transcript_dir, os.W_OK)):
                    self.perror("{!r} is not a directory or you don't have write access".format(transcript_dir))
                    return
                commands_run = 0
                try:
                    with self.sigint_protection:
                        saved_echo = self.echo
                        saved_stdout = self.stdout
                        self.echo = False
                    transcript = ''
                    for history_item in history:
                        first = True
                        command = ''
                        if isinstance(history_item, HistoryItem):
                            history_item = history_item.raw
                        for line in history_item.splitlines():
                            if first:
                                command += '{}{}\n'.format(self.prompt, line)
                                first = False
                            else:
                                command += '{}{}\n'.format(self.continuation_prompt, line)

                        transcript += command
                        self.stdout = utils.StdSim(self.stdout)
                        stop = self.onecmd_plus_hooks(history_item)
                        commands_run += 1
                        transcript += self.stdout.getvalue().replace('/', '\\/')
                        if stop:
                            break

                finally:
                    with self.sigint_protection:
                        self.echo = saved_echo
                        self.stdout = saved_stdout

                if commands_run < len(history):
                    warning = 'Command {} triggered a stop and ended transcript generation early'.format(commands_run)
                    self.perror(ansi.style_warning(warning))
                try:
                    with open(transcript_file, 'w') as (fout):
                        fout.write(transcript)
                except OSError as ex:
                    try:
                        self.pexcept('Failed to save transcript: {}'.format(ex))
                    finally:
                        ex = None
                        del ex

                else:
                    if commands_run > 1:
                        plural = 'commands and their outputs'
                    else:
                        plural = 'command and its output'
                    msg = '{} {} saved to transcript file {!r}'
                    self.pfeedback(msg.format(commands_run, plural, transcript_file))

            edit_description = 'Edit a file in a text editor\n\nThe editor used is determined by a settable parameter. To set it:\n\n  set editor (program-name)'
            edit_parser = ArgParser(description=edit_description)
            edit_parser.add_argument('file_path', nargs=(argparse.OPTIONAL), help='path to a file to open in editor',
              completer_method=path_complete)

            @with_argparser(edit_parser)
            def thgcmd_edit(self, args: argparse.Namespace) -> None:
                """Edit a file in a text editor"""
                if not self.editor:
                    raise EnvironmentError("Please use 'set editor' to specify your text editing program of choice.")
                command = utils.quote_string_if_needed(os.path.expanduser(self.editor))
                if args.file_path:
                    command += ' ' + utils.quote_string_if_needed(os.path.expanduser(args.file_path))
                self.thgcmd_shell(command)

            @property
            def _current_script_dir(self) -> Optional[str]:
                """Accessor to get the current script directory from the _script_dir LIFO queue."""
                if self._script_dir:
                    return self._script_dir[(-1)]
                return

            run_script_description = 'Run commands in script file that is encoded as either ASCII or UTF-8 text\n\nScript should contain one command per line, just like the command would be\ntyped in the console.\n\nIf the -t/--transcript flag is used, this command instead records\nthe output of the script commands to a transcript for testing purposes.\n'
            run_script_parser = ArgParser(description=run_script_description)
            run_script_parser.add_argument('-t', '--transcript', metavar='TRANSCRIPT_FILE', help='record the output of the script as a transcript file',
              completer_method=path_complete)
            run_script_parser.add_argument('script_path', help='path to the script file', completer_method=path_complete)

            @with_argparser(run_script_parser)
            def thgcmd_run_script(self, args: argparse.Namespace) -> Optional[bool]:
                """Run commands in script file that is encoded as either ASCII or UTF-8 text.

        :return: True if running of commands should stop
        """
                expanded_path = os.path.abspath(os.path.expanduser(args.script_path))
                if not os.path.exists(expanded_path):
                    self.perror("'{}' does not exist or cannot be accessed".format(expanded_path))
                    return
                if not os.path.isfile(expanded_path):
                    self.perror("'{}' is not a file".format(expanded_path))
                    return
                if os.path.getsize(expanded_path) == 0:
                    self.perror("'{}' is empty".format(expanded_path))
                    return
                if not utils.is_text_file(expanded_path):
                    self.perror("'{}' is not an ASCII or UTF-8 encoded text file".format(expanded_path))
                    return
                try:
                    with open(expanded_path, encoding='utf-8') as (target):
                        script_commands = target.read().splitlines()
                except OSError as ex:
                    try:
                        self.pexcept("Problem accessing script from '{}': {}".format(expanded_path, ex))
                        return
                    finally:
                        ex = None
                        del ex

                orig_script_dir_count = len(self._script_dir)
                try:
                    self._script_dir.append(os.path.dirname(expanded_path))
                    if args.transcript:
                        self._generate_transcript(script_commands, os.path.expanduser(args.transcript))
                    else:
                        return self.runcmds_plus_hooks(script_commands)
                finally:
                    with self.sigint_protection:
                        if orig_script_dir_count != len(self._script_dir):
                            self._script_dir.pop()

            relative_run_script_description = run_script_description
            relative_run_script_description += "\n\nIf this is called from within an already-running script, the filename will be\ninterpreted relative to the already-running script's directory."
            relative_run_script_epilog = 'Notes:\n  This command is intended to only be used within text file scripts.'
            relative_run_script_parser = ArgParser(description=relative_run_script_description, epilog=relative_run_script_epilog)
            relative_run_script_parser.add_argument('file_path', help='a file path pointing to a script')

            @with_argparser(relative_run_script_parser)
            def thgcmd__relative_run_script(self, args: argparse.Namespace) -> Optional[bool]:
                """
        Run commands in script file that is encoded as either ASCII or UTF-8 text
        :return: True if running of commands should stop
        """
                file_path = args.file_path
                relative_path = os.path.join(self._current_script_dir or '', file_path)
                return self.thgcmd_run_script(relative_path)

            def _run_transcript_tests(self, transcript_paths: List[str]) -> None:
                """Runs transcript tests for provided file(s).

        This is called when either -t is provided on the command line or the transcript_files argument is provided
        during construction of the thgcmd.Cmd instance.

        :param transcript_paths: list of transcript test file paths
        """
                import time, unittest, thgcmd
                from .transcript import Cmd2TestCase

                class TestMyAppCase(Cmd2TestCase):
                    cmdapp = self

                transcripts_expanded = utils.files_from_glob_patterns(transcript_paths, access=(os.R_OK))
                if not transcripts_expanded:
                    self.perror('No test files found - nothing to test')
                    self.exit_code = -1
                    return
                verinfo = '.'.join(map(str, sys.version_info[:3]))
                num_transcripts = len(transcripts_expanded)
                plural = '' if len(transcripts_expanded) == 1 else 's'
                self.poutput(ansi.style(utils.center_text('thgcmd transcript test', pad='='), bold=True))
                self.poutput('platform {} -- Python {}, thgcmd-{}, readline-{}'.format(sys.platform, verinfo, thgcmd.__version__, rl_type))
                self.poutput('cwd: {}'.format(os.getcwd()))
                self.poutput('thgcmd app: {}'.format(sys.argv[0]))
                self.poutput(ansi.style(('collected {} transcript{}'.format(num_transcripts, plural)), bold=True))
                self.__class__.testfiles = transcripts_expanded
                sys.argv = [sys.argv[0]]
                testcase = TestMyAppCase()
                stream = utils.StdSim(sys.stderr)
                runner = unittest.TextTestRunner(stream=stream)
                start_time = time.time()
                test_results = runner.run(testcase)
                execution_time = time.time() - start_time
                if test_results.wasSuccessful():
                    ansi.ansi_aware_write(sys.stderr, stream.read())
                    finish_msg = '{0} transcript{1} passed in {2:.3f} seconds'.format(num_transcripts, plural, execution_time)
                    finish_msg = ansi.style_success(utils.center_text(finish_msg, pad='='))
                    self.poutput(finish_msg)
                else:
                    error_str = stream.read()
                    end_of_trace = error_str.find('AssertionError:')
                    file_offset = error_str[end_of_trace:].find('File ')
                    start = end_of_trace + file_offset
                    self.perror(error_str[start:])
                    self.exit_code = -1

            def async_alert(self, alert_msg: str, new_prompt: Optional[str]=None) -> None:
                """
        Display an important message to the user while they are at the prompt in between commands.
        To the user it appears as if an alert message is printed above the prompt and their current input
        text and cursor location is left alone.

        Raises a `RuntimeError` if called while another thread holds `terminal_lock`.

        IMPORTANT: This function will not print an alert unless it can acquire self.terminal_lock to ensure
                   a prompt is onscreen.  Therefore it is best to acquire the lock before calling this function
                   to guarantee the alert prints.

        :param alert_msg: the message to display to the user
        :param new_prompt: if you also want to change the prompt that is displayed, then include it here
                           see async_update_prompt() docstring for guidance on updating a prompt
        """
                if vt100_support:
                    return self.use_rawinput or None
                elif self.terminal_lock.acquire(blocking=False):
                    current_prompt = self.continuation_prompt if self._at_continuation_prompt else self.prompt
                    update_terminal = False
                    if alert_msg:
                        alert_msg += '\n'
                        update_terminal = True
                    if new_prompt is not None:
                        if new_prompt != self.prompt:
                            self.prompt = new_prompt
                            if not self._at_continuation_prompt:
                                rl_set_prompt(self.prompt)
                                update_terminal = True
                    if update_terminal:
                        import shutil
                        terminal_str = ansi.async_alert_str(terminal_columns=(shutil.get_terminal_size().columns), prompt=current_prompt,
                          line=(readline.get_line_buffer()),
                          cursor_offset=(rl_get_point()),
                          alert_msg=alert_msg)
                        if rl_type == RlType.GNU:
                            sys.stderr.write(terminal_str)
                        else:
                            if rl_type == RlType.PYREADLINE:
                                readline.rl.mode.console.write(terminal_str)
                        rl_force_redisplay()
                    self.terminal_lock.release()
                else:
                    raise RuntimeError('another thread holds terminal_lock')

            def async_update_prompt(self, new_prompt: str) -> None:
                """
        Update the prompt while the user is still typing at it. This is good for alerting the user to system
        changes dynamically in between commands. For instance you could alter the color of the prompt to indicate
        a system status or increase a counter to report an event. If you do alter the actual text of the prompt,
        it is best to keep the prompt the same width as what's on screen. Otherwise the user's input text will
        be shifted and the update will not be seamless.

        Raises a `RuntimeError` if called while another thread holds `terminal_lock`.

        IMPORTANT: This function will not update the prompt unless it can acquire self.terminal_lock to ensure
                   a prompt is onscreen.  Therefore it is best to acquire the lock before calling this function
                   to guarantee the prompt changes.

                   If a continuation prompt is currently being displayed while entering a multiline
                   command, the onscreen prompt will not change. However self.prompt will still be updated
                   and display immediately after the multiline line command completes.

        :param new_prompt: what to change the prompt to
        """
                self.async_alert('', new_prompt)

            def set_window_title(self, title: str) -> None:
                """Set the terminal window title.

        Raises a `RuntimeError` if called while another thread holds `terminal_lock`.

        IMPORTANT: This function will not set the title unless it can acquire self.terminal_lock to avoid
                   writing to stderr while a command is running. Therefore it is best to acquire the lock
                   before calling this function to guarantee the title changes.

        :param title: the new window title
        """
                if not vt100_support:
                    return
                elif self.terminal_lock.acquire(blocking=False):
                    try:
                        try:
                            sys.stderr.write(ansi.set_title_str(title))
                        except AttributeError:
                            pass

                    finally:
                        self.terminal_lock.release()

                else:
                    raise RuntimeError('another thread holds terminal_lock')

            def enable_command(self, command: str) -> None:
                """
        Enable a command by restoring its functions
        :param command: the command being enabled
        """
                if command not in self.disabled_commands:
                    return
                else:
                    help_func_name = HELP_FUNC_PREFIX + command
                    dc = self.disabled_commands[command]
                    setattr(self, self._cmd_func_name(command), dc.command_function)
                    if dc.help_function is None:
                        delattr(self, help_func_name)
                    else:
                        setattr(self, help_func_name, dc.help_function)
                del self.disabled_commands[command]

            def enable_category(self, category: str) -> None:
                """
        Enable an entire category of commands
        :param category: the category to enable
        """
                for cmd_name in list(self.disabled_commands):
                    func = self.disabled_commands[cmd_name].command_function
                    if hasattr(func, HELP_CATEGORY) and getattr(func, HELP_CATEGORY) == category:
                        self.enable_command(cmd_name)

            def disable_command(self, command: str, message_to_print: str) -> None:
                """
        Disable a command and overwrite its functions
        :param command: the command being disabled
        :param message_to_print: what to print when this command is run or help is called on it while disabled

                                 The variable COMMAND_NAME can be used as a placeholder for the name of the
                                 command being disabled.
                                 ex: message_to_print = "{} is currently disabled".format(COMMAND_NAME)
        """
                import functools
                if command in self.disabled_commands:
                    return
                command_function = self.cmd_func(command)
                if command_function is None:
                    raise AttributeError('{} does not refer to a command'.format(command))
                help_func_name = HELP_FUNC_PREFIX + command
                self.disabled_commands[command] = DisabledCommand(command_function=command_function, help_function=(getattr(self, help_func_name, None)))
                new_func = functools.partial((self._report_disabled_command_usage), message_to_print=(message_to_print.replace(COMMAND_NAME, command)))
                setattr(self, self._cmd_func_name(command), new_func)
                setattr(self, help_func_name, new_func)

            def disable_category(self, category: str, message_to_print: str) -> None:
                """Disable an entire category of commands.

        :param category: the category to disable
        :param message_to_print: what to print when anything in this category is run or help is called on it
                                 while disabled. The variable COMMAND_NAME can be used as a placeholder for the name
                                 of the command being disabled.
                                 ex: message_to_print = "{} is currently disabled".format(COMMAND_NAME)
        """
                all_commands = self.get_all_commands()
                for cmd_name in all_commands:
                    func = self.cmd_func(cmd_name)
                    if hasattr(func, HELP_CATEGORY) and getattr(func, HELP_CATEGORY) == category:
                        self.disable_command(cmd_name, message_to_print)

            @staticmethod
            def _report_disabled_command_usage(*args, message_to_print: str, **kwargs) -> None:
                """
        Report when a disabled command has been run or had help called on it
        :param args: not used
        :param message_to_print: the message reporting that the command is disabled
        :param kwargs: not used
        """
                ansi.ansi_aware_write(sys.stderr, '{}\n'.format(message_to_print))

            def cmdloop(self, intro: Optional[str]=None) -> int:
                """This is an outer wrapper around _cmdloop() which deals with extra features provided by thgcmd.

        _cmdloop() provides the main loop equivalent to cmd.cmdloop().  This is a wrapper around that which deals with
        the following extra features provided by thgcmd:
        - transcript testing
        - intro banner
        - exit code

        :param intro: if provided this overrides self.intro and serves as the intro banner printed once at start
        """
                if threading.current_thread() is not threading.main_thread():
                    raise RuntimeError('cmdloop must be run in the main thread')
                import signal
                original_sigint_handler = signal.getsignal(signal.SIGINT)
                signal.signal(signal.SIGINT, self.sigint_handler)
                self.terminal_lock.acquire()
                for func in self._preloop_hooks:
                    func()

                self.preloop()
                if self._transcript_files is not None:
                    self._run_transcript_tests([os.path.expanduser(tf) for tf in self._transcript_files])
                else:
                    if intro is not None:
                        self.intro = intro
                    if self.intro is not None:
                        self.poutput(self.intro)
                    self._cmdloop()
                for func in self._postloop_hooks:
                    func()

                self.postloop()
                self.terminal_lock.release()
                signal.signal(signal.SIGINT, original_sigint_handler)
                return self.exit_code

            def _initialize_plugin_system(self) -> None:
                """Initialize the plugin system"""
                self._preloop_hooks = []
                self._postloop_hooks = []
                self._postparsing_hooks = []
                self._precmd_hooks = []
                self._postcmd_hooks = []
                self._cmdfinalization_hooks = []

            @classmethod
            def _validate_callable_param_count(cls, func: Callable, count: int) -> None:
                """Ensure a function has the given number of parameters."""
                signature = inspect.signature(func)
                nparam = len(signature.parameters)
                if nparam != count:
                    raise TypeError('{} has {} positional arguments, expected {}'.format(func.__name__, nparam, count))

            @classmethod
            def _validate_prepostloop_callable(cls, func: Callable[([None], None)]) -> None:
                """Check parameter and return types for preloop and postloop hooks."""
                cls._validate_callable_param_count(func, 0)
                signature = inspect.signature(func)
                if signature.return_annotation is not None:
                    raise TypeError("{} must declare return a return type of 'None'".format(func.__name__))

            def register_preloop_hook(self, func: Callable[([None], None)]) -> None:
                """Register a function to be called at the beginning of the command loop."""
                self._validate_prepostloop_callable(func)
                self._preloop_hooks.append(func)

            def register_postloop_hook(self, func: Callable[([None], None)]) -> None:
                """Register a function to be called at the end of the command loop."""
                self._validate_prepostloop_callable(func)
                self._postloop_hooks.append(func)

            @classmethod
            def _validate_postparsing_callable(cls, func: Callable[([plugin.PostparsingData], plugin.PostparsingData)]) -> None:
                """Check parameter and return types for postparsing hooks"""
                cls._validate_callable_param_count(func, 1)
                signature = inspect.signature(func)
                _, param = list(signature.parameters.items())[0]
                if param.annotation != plugin.PostparsingData:
                    raise TypeError("{} must have one parameter declared with type 'thgcmd.plugin.PostparsingData'".format(func.__name__))
                if signature.return_annotation != plugin.PostparsingData:
                    raise TypeError("{} must declare return a return type of 'thgcmd.plugin.PostparsingData'".format(func.__name__))

            def register_postparsing_hook(self, func: Callable[([plugin.PostparsingData], plugin.PostparsingData)]) -> None:
                """Register a function to be called after parsing user input but before running the command"""
                self._validate_postparsing_callable(func)
                self._postparsing_hooks.append(func)

            @classmethod
            def _validate_prepostcmd_hook(cls, func: Callable, data_type: Type) -> None:
                """Check parameter and return types for pre and post command hooks."""
                signature = inspect.signature(func)
                cls._validate_callable_param_count(func, 1)
                paramname = list(signature.parameters.keys())[0]
                param = signature.parameters[paramname]
                if param.annotation != data_type:
                    raise TypeError('argument 1 of {} has incompatible type {}, expected {}'.format(func.__name__, param.annotation, data_type))
                if signature.return_annotation == signature.empty:
                    raise TypeError('{} does not have a declared return type, expected {}'.format(func.__name__, data_type))
                if signature.return_annotation != data_type:
                    raise TypeError('{} has incompatible return type {}, expected {}'.format(func.__name__, signature.return_annotation, data_type))

            def register_precmd_hook(self, func: Callable[([plugin.PrecommandData], plugin.PrecommandData)]) -> None:
                """Register a hook to be called before the command function."""
                self._validate_prepostcmd_hook(func, plugin.PrecommandData)
                self._precmd_hooks.append(func)

            def register_postcmd_hook(self, func: Callable[([plugin.PostcommandData], plugin.PostcommandData)]) -> None:
                """Register a hook to be called after the command function."""
                self._validate_prepostcmd_hook(func, plugin.PostcommandData)
                self._postcmd_hooks.append(func)

            @classmethod
            def _validate_cmdfinalization_callable(cls, func: Callable[([plugin.CommandFinalizationData],
 plugin.CommandFinalizationData)]) -> None:
                """Check parameter and return types for command finalization hooks."""
                cls._validate_callable_param_count(func, 1)
                signature = inspect.signature(func)
                _, param = list(signature.parameters.items())[0]
                if param.annotation != plugin.CommandFinalizationData:
                    raise TypeError("{} must have one parameter declared with type 'thgcmd.plugin.CommandFinalizationData'".format(func.__name__))
                if signature.return_annotation != plugin.CommandFinalizationData:
                    raise TypeError("{} must declare return a return type of 'thgcmd.plugin.CommandFinalizationData'".format(func.__name__))

            def register_cmdfinalization_hook(self, func: Callable[([plugin.CommandFinalizationData],
 plugin.CommandFinalizationData)]) -> None:
                """Register a hook to be called after a command is completed, whether it completes successfully or not."""
                self._validate_cmdfinalization_callable(func)
                self._cmdfinalization_hooks.append(func)