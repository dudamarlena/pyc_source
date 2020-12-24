# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/parsing.py
# Compiled at: 2019-07-17 15:13:04
# Size of source mod 2**32: 29608 bytes
"""Statement parsing classes for thgcmd"""
import re, shlex
from typing import Dict, Iterable, List, Optional, Tuple, Union
import attr
from . import constants
from . import utils

def shlex_split(str_to_split: str) -> List[str]:
    """A wrapper around shlex.split() that uses thgcmd's preferred arguments.

    This allows other classes to easily call split() the same way StatementParser does
    :param str_to_split: the string being split
    :return: A list of tokens
    """
    return shlex.split(str_to_split, comments=False, posix=False)


@attr.s(frozen=True)
class MacroArg:
    __doc__ = '\n    Information used to replace or unescape arguments in a macro value when the macro is resolved\n    Normal argument syntax  : {5}\n    Escaped argument syntax: {{5}}\n    '
    start_index = attr.ib(validator=(attr.validators.instance_of(int)))
    number_str = attr.ib(validator=(attr.validators.instance_of(str)))
    is_escaped = attr.ib(validator=(attr.validators.instance_of(bool)))
    macro_normal_arg_pattern = re.compile('(?<!{){\\d+}|{\\d+}(?!})')
    macro_escaped_arg_pattern = re.compile('{{2}\\d+}{2}')
    digit_pattern = re.compile('\\d+')


@attr.s(frozen=True)
class Macro:
    __doc__ = 'Defines a thgcmd macro'
    name = attr.ib(validator=(attr.validators.instance_of(str)))
    value = attr.ib(validator=(attr.validators.instance_of(str)))
    minimum_arg_count = attr.ib(validator=(attr.validators.instance_of(int)))
    arg_list = attr.ib(default=(attr.Factory(list)), validator=(attr.validators.instance_of(list)))


@attr.s(frozen=True)
class Statement(str):
    __doc__ = "String subclass with additional attributes to store the results of parsing.\n\n    The cmd module in the standard library passes commands around as a\n    string. To retain backwards compatibility, thgcmd does the same. However, we\n    need a place to capture the additional output of the command parsing, so we add\n    our own attributes to this subclass.\n\n    Instances of this class should not be created by anything other than the\n    `StatementParser.parse()` method, nor should any of the attributes be modified\n    once the object is created.\n\n    The string portion of the class contains the arguments, but not the command, nor\n    the output redirection clauses.\n\n    Here's some suggestions and best practices for how to use the attributes of this\n    object:\n\n    command - the name of the command, shortcuts and aliases have already been\n              expanded\n\n    args - the arguments to the command, excluding output redirection and command\n           terminators. If the user used quotes in their input, they remain here,\n           and you will have to handle them on your own.\n\n    arg_list - the arguments to the command, excluding output redirection and\n               command terminators. Each argument is represented as an element\n               in the list. Quoted arguments remain quoted. If you want to\n               remove the quotes, use `thgcmd.utils.strip_quotes()` or use\n               `argv[1:]`\n\n    command_and_args - join the args and the command together with a space. Output\n                       redirection is excluded.\n\n    argv - this is a list of arguments in the style of `sys.argv`. The first element\n           of the list is the command. Subsequent elements of the list contain any\n           additional arguments, with quotes removed, just like bash would. This\n           is very useful if you are going to use `argparse.parse_args()`:\n           ```\n           def do_mycommand(stmt):\n               mycommand_argparser.parse_args(stmt.argv)\n               ...\n            ```\n\n    raw - if you want full access to exactly what the user typed at the input prompt\n          you can get it, but you'll have to parse it on your own, including:\n             - shortcuts and aliases\n             - quoted commands and arguments\n             - output redirection\n             - multi-line command terminator handling\n          if you use multiline commands, all the input will be passed to you in\n          this string, but there will be embedded newlines where\n          the user hit return to continue the command on the next line.\n\n    Tips:\n\n    1. `argparse` is your friend for anything complex. `thgcmd` has two decorators\n       (`with_argparser`, and `with_argparser_and_unknown_args`) which you can use\n       to make your command method receive a namespace of parsed arguments, whether\n       positional or denoted with switches.\n\n    2. For commands with simple positional arguments, use `args` or `arg_list`\n\n    3. If you don't want to have to worry about quoted arguments, use\n       argv[1:], which strips them all off for you.\n    "
    args = attr.ib(default='', validator=(attr.validators.instance_of(str)))
    raw = attr.ib(default='', validator=(attr.validators.instance_of(str)))
    command = attr.ib(default='', validator=(attr.validators.instance_of(str)))
    arg_list = attr.ib(default=(attr.Factory(list)), validator=(attr.validators.instance_of(list)))
    multiline_command = attr.ib(default='', validator=(attr.validators.instance_of(str)))
    terminator = attr.ib(default='', validator=(attr.validators.instance_of(str)))
    suffix = attr.ib(default='', validator=(attr.validators.instance_of(str)))
    pipe_to = attr.ib(default='', validator=(attr.validators.instance_of(str)))
    output = attr.ib(default='', validator=(attr.validators.instance_of(str)))
    output_to = attr.ib(default='', validator=(attr.validators.instance_of(str)))

    def __new__(cls, value, *pos_args, **kw_args):
        """Create a new instance of Statement.

        We must override __new__ because we are subclassing `str` which is
        immutable and takes a different number of arguments as Statement.

        NOTE:  attrs takes care of initializing other members in the __init__ it
        generates.
        """
        stmt = super().__new__(cls, value)
        return stmt

    @property
    def command_and_args(self) -> str:
        """Combine command and args with a space separating them.

        Quoted arguments remain quoted. Output redirection and piping are
        excluded, as are any multiline command terminators.
        """
        if self.command and self.args:
            rtn = '{} {}'.format(self.command, self.args)
        else:
            if self.command:
                rtn = self.command
            else:
                rtn = ''
        return rtn

    @property
    def post_command(self) -> str:
        """A string containing any ending terminator, suffix, and redirection chars"""
        rtn = ''
        if self.terminator:
            rtn += self.terminator
        if self.suffix:
            rtn += ' ' + self.suffix
        if self.pipe_to:
            rtn += ' | ' + self.pipe_to
        if self.output:
            rtn += ' ' + self.output
            if self.output_to:
                rtn += ' ' + self.output_to
        return rtn

    @property
    def expanded_command_line(self) -> str:
        """Combines command_and_args and post_command"""
        return self.command_and_args + self.post_command

    @property
    def argv(self) -> List[str]:
        """a list of arguments a la sys.argv.

        Quotes, if any, are removed from the elements of the list, and aliases
        and shortcuts are expanded
        """
        if self.command:
            rtn = [
             utils.strip_quotes(self.command)]
            for cur_token in self.arg_list:
                rtn.append(utils.strip_quotes(cur_token))

        else:
            rtn = []
        return rtn


class StatementParser:
    __doc__ = 'Parse raw text into command components.\n\n    Shortcuts is a list of tuples with each tuple containing the shortcut and\n    the expansion.\n    '

    def __init__(self, allow_redirection: bool=True, terminators: Optional[Iterable[str]]=None, multiline_commands: Optional[Iterable[str]]=None, aliases: Optional[Dict[(str, str)]]=None, shortcuts: Optional[Dict[(str, str)]]=None) -> None:
        """Initialize an instance of StatementParser.

        The following will get converted to an immutable tuple before storing internally:
        * terminators
        * multiline commands
        * shortcuts

        :param allow_redirection: should redirection and pipes be allowed?
        :param terminators: iterable containing strings which should terminate multiline commands
        :param multiline_commands: iterable containing the names of commands that accept multiline input
        :param aliases: dictionary containing aliases
        :param shortcuts: dictionary containing shortcuts
        """
        self.allow_redirection = allow_redirection
        if terminators is None:
            self.terminators = (
             constants.MULTILINE_TERMINATOR,)
        else:
            self.terminators = tuple(terminators)
        if multiline_commands is None:
            self.multiline_commands = tuple()
        else:
            self.multiline_commands = tuple(multiline_commands)
        if aliases is None:
            self.aliases = dict()
        else:
            self.aliases = aliases
        if shortcuts is None:
            shortcuts = constants.DEFAULT_SHORTCUTS
        self.shortcuts = tuple(sorted((shortcuts.items()), key=(lambda x: len(x[0])), reverse=True))
        invalid_command_chars = []
        invalid_command_chars.extend(constants.QUOTES)
        invalid_command_chars.extend(constants.REDIRECTION_CHARS)
        invalid_command_chars.extend(self.terminators)
        second_group_items = [re.escape(x) for x in invalid_command_chars]
        second_group_items.extend(['\\s', '\\Z'])
        second_group = '|'.join(second_group_items)
        expr = '\\A\\s*(\\S*?)({})'.format(second_group)
        self._command_pattern = re.compile(expr)

    def is_valid_command(self, word: str) -> Tuple[(bool, str)]:
        """Determine whether a word is a valid name for a command.

        Commands can not include redirection characters, whitespace,
        or termination characters. They also cannot start with a
        shortcut.

        If word is not a valid command, return False and error text
        This string is suitable for inclusion in an error message of your
        choice:

        valid, errmsg = statement_parser.is_valid_command('>')
        if not valid:
            errmsg = "Alias {}".format(errmsg)
        """
        valid = False
        if not word:
            return (False, 'cannot be an empty string')
        if word.startswith(constants.COMMENT_CHAR):
            return (False, 'cannot start with the comment character')
        for shortcut, _ in self.shortcuts:
            if word.startswith(shortcut):
                errmsg = 'cannot start with a shortcut: '
                errmsg += ', '.join((shortcut for shortcut, _ in self.shortcuts))
                return (False, errmsg)

        errmsg = 'cannot contain: whitespace, quotes, '
        errchars = []
        errchars.extend(constants.REDIRECTION_CHARS)
        errchars.extend(self.terminators)
        errmsg += ', '.join([shlex.quote(x) for x in errchars])
        match = self._command_pattern.search(word)
        if match:
            if word == match.group(1):
                valid = True
                errmsg = ''
        return (
         valid, errmsg)

    def tokenize(self, line: str, expand: bool=True) -> List[str]:
        """
        Lex a string into a list of tokens. Shortcuts and aliases are expanded and comments are removed

        :param line: the command line being lexed
        :param expand: If True, then aliases and shortcuts will be expanded.
                       Set this to False if no expansion should occur because the command name is already known.
                       Otherwise the command could be expanded if it matched an alias name. This is for cases where
                       a do_* method was called manually (e.g do_help('alias').
        :return: A list of tokens
        :raises ValueError if there are unclosed quotation marks.
        """
        if expand:
            line = self._expand(line)
        if line.lstrip().startswith(constants.COMMENT_CHAR):
            return []
        tokens = shlex_split(line)
        tokens = self._split_on_punctuation(tokens)
        return tokens

    def parse(self, line: str, expand: bool=True) -> Statement:
        """
        Tokenize the input and parse it into a Statement object, stripping
        comments, expanding aliases and shortcuts, and extracting output
        redirection directives.

        :param line: the command line being parsed
        :param expand: If True, then aliases and shortcuts will be expanded.
                       Set this to False if no expansion should occur because the command name is already known.
                       Otherwise the command could be expanded if it matched an alias name. This is for cases where
                       a do_* method was called manually (e.g do_help('alias').
        :return: A parsed Statement
        :raises ValueError if there are unclosed quotation marks
        """
        terminator = ''
        if line[-1:] == constants.LINE_FEED:
            terminator = constants.LINE_FEED
        command = ''
        args = ''
        arg_list = []
        tokens = self.tokenize(line, expand)
        terminator_pos = len(tokens) + 1
        for pos, cur_token in enumerate(tokens):
            for test_terminator in self.terminators:
                if cur_token.startswith(test_terminator):
                    terminator_pos = pos
                    terminator = test_terminator
                    break
            else:
                continue

            break

        if terminator:
            if terminator == constants.LINE_FEED:
                terminator_pos = len(tokens) + 1
            command, args = self._command_and_args(tokens[:terminator_pos])
            arg_list = tokens[1:terminator_pos]
            tokens = tokens[terminator_pos + 1:]
        else:
            testcommand, testargs = self._command_and_args(tokens)
            if testcommand in self.multiline_commands:
                command = testcommand
                args = testargs
                arg_list = tokens[1:]
                tokens = []
            else:
                pipe_to = ''
                output = ''
                output_to = ''
                try:
                    pipe_index = tokens.index(constants.REDIRECTION_PIPE)
                except ValueError:
                    pipe_index = len(tokens)

            try:
                redir_index = tokens.index(constants.REDIRECTION_OUTPUT)
            except ValueError:
                redir_index = len(tokens)

            try:
                append_index = tokens.index(constants.REDIRECTION_APPEND)
            except ValueError:
                append_index = len(tokens)

            if pipe_index < redir_index and pipe_index < append_index:
                pipe_to_tokens = tokens[pipe_index + 1:]
                utils.expand_user_in_tokens(pipe_to_tokens)
                pipe_to = ' '.join(pipe_to_tokens)
                tokens = tokens[:pipe_index]
            else:
                if redir_index != append_index:
                    if redir_index < append_index:
                        output = constants.REDIRECTION_OUTPUT
                        output_index = redir_index
                    else:
                        output = constants.REDIRECTION_APPEND
                        output_index = append_index
                    if len(tokens) > output_index + 1:
                        unquoted_path = utils.strip_quotes(tokens[(output_index + 1)])
                        if unquoted_path:
                            output_to = utils.expand_user(tokens[(output_index + 1)])
                    tokens = tokens[:output_index]
        if terminator:
            suffix = ' '.join(tokens)
        else:
            suffix = ''
            if not command:
                command, args = self._command_and_args(tokens)
                arg_list = tokens[1:]
            elif command in self.multiline_commands:
                multiline_command = command
            else:
                multiline_command = ''
            statement = Statement(args, raw=line,
              command=command,
              arg_list=arg_list,
              multiline_command=multiline_command,
              terminator=terminator,
              suffix=suffix,
              pipe_to=pipe_to,
              output=output,
              output_to=output_to)
            return statement

    def parse_command_only(self, rawinput: str) -> Statement:
        """Partially parse input into a Statement object.

        The command is identified, and shortcuts and aliases are expanded.
        Multiline commands are identified, but terminators and output
        redirection are not parsed.

        This method is used by tab completion code and therefore must not
        generate an exception if there are unclosed quotes.

        The `Statement` object returned by this method can at most contain values
        in the following attributes:
          - args
          - raw
          - command
          - multiline_command

        `Statement.args` includes all output redirection clauses and command
        terminators.

        Different from parse(), this method does not remove redundant whitespace
        within args. However, it does ensure args has no leading or trailing
        whitespace.
        """
        line = self._expand(rawinput)
        command = ''
        args = ''
        match = self._command_pattern.search(line)
        if match:
            command = match.group(1)
            args = line[match.end(1):].strip()
            args = command and args or ''
        elif command in self.multiline_commands:
            multiline_command = command
        else:
            multiline_command = ''
        statement = Statement(args, raw=rawinput,
          command=command,
          multiline_command=multiline_command)
        return statement

    def get_command_arg_list(self, command_name: str, to_parse: Union[(Statement, str)], preserve_quotes: bool) -> Tuple[(Statement, List[str])]:
        """
        Called by the argument_list and argparse wrappers to retrieve just the arguments being
        passed to their do_* methods as a list.

        :param command_name: name of the command being run
        :param to_parse: what is being passed to the do_* method. It can be one of two types:
                         1. An already parsed Statement
                         2. An argument string in cases where a do_* method is explicitly called
                            e.g.: Calling do_help('alias create') would cause to_parse to be 'alias create'

                            In this case, the string will be converted to a Statement and returned along
                            with the argument list.

        :param preserve_quotes: if True, then quotes will not be stripped from the arguments
        :return: A tuple containing:
                    The Statement used to retrieve the arguments
                    The argument list
        """
        if not isinstance(to_parse, Statement):
            to_parse = self.parse((command_name + ' ' + to_parse), expand=False)
        if preserve_quotes:
            return (
             to_parse, to_parse.arg_list)
        return (to_parse, to_parse.argv[1:])

    def _expand(self, line: str) -> str:
        """Expand aliases and shortcuts"""
        remaining_aliases = list(self.aliases.keys())
        keep_expanding = bool(remaining_aliases)
        while keep_expanding:
            keep_expanding = False
            match = self._command_pattern.search(line)
            if match:
                command = match.group(1)
                if command in remaining_aliases:
                    line = self.aliases[command] + match.group(2) + line[match.end(2):]
                    remaining_aliases.remove(command)
                    keep_expanding = bool(remaining_aliases)

        for shortcut, expansion in self.shortcuts:
            if line.startswith(shortcut):
                shortcut_len = len(shortcut)
                if len(line) == shortcut_len or line[shortcut_len] != ' ':
                    expansion += ' '
                line = line.replace(shortcut, expansion, 1)
                break

        return line

    @staticmethod
    def _command_and_args(tokens: List[str]) -> Tuple[(str, str)]:
        """Given a list of tokens, return a tuple of the command
        and the args as a string.
        """
        command = ''
        args = ''
        if tokens:
            command = tokens[0]
        if len(tokens) > 1:
            args = ' '.join(tokens[1:])
        return (command, args)

    def _split_on_punctuation(self, tokens: List[str]) -> List[str]:
        """Further splits tokens from a command line using punctuation characters

        Punctuation characters are treated as word breaks when they are in
        unquoted strings. Each run of punctuation characters is treated as a
        single token.

        :param tokens: the tokens as parsed by shlex
        :return: the punctuated tokens
        """
        punctuation = []
        punctuation.extend(self.terminators)
        if self.allow_redirection:
            punctuation.extend(constants.REDIRECTION_CHARS)
        punctuated_tokens = []
        for cur_initial_token in tokens:
            if not len(cur_initial_token) <= 1:
                if cur_initial_token[0] in constants.QUOTES:
                    punctuated_tokens.append(cur_initial_token)
                    continue
                cur_index = 0
                cur_char = cur_initial_token[cur_index]
                new_token = ''
                while True:
                    if cur_char not in punctuation:
                        while cur_char not in punctuation:
                            new_token += cur_char
                            cur_index += 1
                            if cur_index < len(cur_initial_token):
                                cur_char = cur_initial_token[cur_index]
                            else:
                                break

                    else:
                        cur_punc = cur_char
                        while cur_char == cur_punc:
                            new_token += cur_char
                            cur_index += 1
                            if cur_index < len(cur_initial_token):
                                cur_char = cur_initial_token[cur_index]
                            else:
                                break

                    punctuated_tokens.append(new_token)
                    new_token = ''
                    if cur_index >= len(cur_initial_token):
                        break

        return punctuated_tokens