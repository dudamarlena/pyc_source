# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/argparse_custom.py
# Compiled at: 2019-07-17 15:13:04
# Size of source mod 2**32: 32141 bytes
"""
This module adds capabilities to argparse by patching a few of its functions. It also defines a parser
class called ArgParser which improves error and help output over normal argparse. All thgcmd code uses
this parser and it is recommended that developers of thgcmd-based apps either use it or write their own parser
that inherits from it. This will give a consistent look-and-feel between the help/error output of built-in
thgcmd commands and the app-specific commands.

Since the new capabilities are added by patching at the argparse API level, they are available whether or
not ArgParser is used. However, the help and error output of ArgParser is customized to notate nargs ranges
whereas any other parser class won't be as explicit in their output.

############################################################################################################
# Added capabilities
############################################################################################################

Extends argparse nargs functionality by allowing tuples which specify a range (min, max). To specify a max
value with no upper bound, use a 1-item tuple (min,)

    Example:
        # -f argument expects at least 3 values
        parser.add_argument('-f', nargs=(3,))

        # -f argument expects 3 to 5 values
        parser.add_argument('-f', nargs=(3, 5))

Tab Completion:
    thgcmd uses its AutoCompleter class to enable argparse-based tab completion on all commands that use the
    @with_argparse wrappers. Out of the box you get tab completion of commands, sub-commands, and flag names,
    as well as instructive hints about the current argument that print when tab is pressed. In addition,
    you can add tab completion for each argument's values using parameters passed to add_argument().

    Below are the 5 add_argument() parameters for enabling tab completion of an argument's value. Only one
    can be used at a time.

    choices
        Pass a list of values to the choices parameter.
        Example:
            parser.add_argument('-o', '--options', choices=['An Option', 'SomeOtherOption'])
            parser.add_argument('-o', '--options', choices=my_list)

    choices_function
        Pass a function that returns choices. This is good in cases where the choice list is dynamically
        generated when the user hits tab.

        Example:
            def my_choices_function):
                ...
                return my_generated_list

            parser.add_argument('-o', '--options', choices_function=my_choices_function)

    choices_method
        This is exactly like choices_function, but the function needs to be an instance method of a thgcmd-based class.
        When AutoCompleter calls the method, it will pass the app instance as the self argument. This is good in
        cases where the list of choices being generated relies on state data of the thgcmd-based app

        Example:
            def my_choices_method(self):
                ...
                return my_generated_list

    completer_function
        Pass a tab-completion function that does custom completion. Since custom tab completion operations commonly
        need to modify thgcmd's instance variables related to tab-completion, it will be rare to need a completer
        function. completer_method should be used in those cases.

        Example:
            def my_completer_function(text, line, begidx, endidx):
                ...
                return completions
            parser.add_argument('-o', '--options', completer_function=my_completer_function)

    completer_method
        This is exactly like completer_function, but the function needs to be an instance method of a thgcmd-based class.
        When AutoCompleter calls the method, it will pass the app instance as the self argument. thgcmd provides
        a few completer methods for convenience (e.g., path_complete, delimiter_complete)

        Example:
            This adds file-path completion to an argument
            parser.add_argument('-o', '--options', completer_method=thgcmd.Cmd.path_complete)

    In all cases in which function/methods are passed you can use functools.partial() to prepopulate
    values of the underlying function.

        Example:
            This says to call path_complete with a preset value for its path_filter argument.
            completer_method = functools.partial(path_complete,
                                                 path_filter=lambda path: os.path.isdir(path))
            parser.add_argument('-o', '--options', choices_method=completer_method)

CompletionItem Class:
    This class was added to help in cases where uninformative data is being tab completed. For instance,
    tab completing ID numbers isn't very helpful to a user without context. Returning a list of CompletionItems
    instead of a regular string for completion results will signal the AutoCompleter to output the completion
    results in a table of completion tokens with descriptions instead of just a table of tokens.

    Instead of this:
        1     2     3

    The user sees this:
        ITEM_ID     Item Name
        1           My item
        2           Another item
        3           Yet another item

    The left-most column is the actual value being tab completed and its header is that value's name.
    The right column header is defined using the descriptive_header parameter of add_argument(). The right
    column values come from the CompletionItem.description value.

    Example:
        token = 1
        token_description = "My Item"
        completion_item = CompletionItem(token, token_description)

    Since descriptive_header and CompletionItem.description are just strings, you can format them in
    such a way to have multiple columns.

    ITEM_ID     Item Name            Checked Out    Due Date
    1           My item              True           02/02/2022
    2           Another item         False
    3           Yet another item     False

    To use CompletionItems, just return them from your choices or completer functions.

    To avoid printing a ton of information to the screen at once when a user presses tab, there is
    a maximum threshold for the number of CompletionItems that will be shown. It's value is defined
    in thgcmd.Cmd.max_completion_items. It defaults to 50, but can be changed. If the number of completion
    suggestions exceeds this number, they will be displayed in the typical columnized format and will
    not include the description value of the CompletionItems.

############################################################################################################
# Patched argparse functions:
###########################################################################################################
argparse._ActionsContainer.add_argument - adds arguments related to tab completion and enables nargs range parsing
                                          See _add_argument_wrapper for more details on these argument

argparse.ArgumentParser._get_nargs_pattern - adds support to for nargs ranges
                                             See _get_nargs_pattern_wrapper for more details

argparse.ArgumentParser._match_argument - adds support to for nargs ranges
                                          See _match_argument_wrapper for more details
"""
import argparse, re, sys
from argparse import ZERO_OR_MORE, ONE_OR_MORE, ArgumentError, _
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union
from .ansi import ansi_aware_write, style_error
INFINITY = float('inf')
ATTR_NARGS_RANGE = 'nargs_range'
ATTR_CHOICES_CALLABLE = 'choices_callable'
ATTR_SUPPRESS_TAB_HINT = 'suppress_tab_hint'
ATTR_DESCRIPTIVE_COMPLETION_HEADER = 'desc_completion_header'

def generate_range_error(range_min: int, range_max: Union[(int, float)]) -> str:
    """Generate an error message when the the number of arguments provided is not within the expected range"""
    err_str = 'expected '
    if range_max == INFINITY:
        err_str += 'at least {} argument'.format(range_min)
        if range_min != 1:
            err_str += 's'
    else:
        if range_min == range_max:
            err_str += '{} argument'.format(range_min)
        else:
            err_str += '{} to {} argument'.format(range_min, range_max)
        if range_max != 1:
            err_str += 's'
    return err_str


class CompletionItem(str):
    __doc__ = '\n    Completion item with descriptive text attached\n\n    See header of this file for more information\n    '

    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, value)

    def __init__(self, value, desc='', *args, **kwargs):
        """
        CompletionItem Initializer

        :param value: the value being tab completed
        :param desc: description text to display
        :param args: args for str __init__
        :param kwargs: kwargs for str __init__
        """
        (super().__init__)(*args, **kwargs)
        self.description = desc


class ChoicesCallable:
    __doc__ = '\n    Enables using a callable as the choices provider for an argparse argument.\n    While argparse has the built-in choices attribute, it is limited to an iterable.\n    '

    def __init__(self, is_method: bool, is_completer: bool, to_call: Callable):
        """
        Initializer
        :param is_method: True if to_call is an instance method of a thgcmd app. False if it is a function.
        :param is_completer: True if to_call is a tab completion routine which expects
                             the args: text, line, begidx, endidx
        :param to_call: the callable object that will be called to provide choices for the argument
        """
        self.is_method = is_method
        self.is_completer = is_completer
        self.to_call = to_call


orig_actions_container_add_argument = argparse._ActionsContainer.add_argument

def _add_argument_wrapper(self, *args, nargs: Union[(int, str, Tuple[int], Tuple[(int, int)], None)]=None, choices_function: Optional[Callable[([], Iterable[Any])]]=None, choices_method: Optional[Callable[([Any], Iterable[Any])]]=None, completer_function: Optional[Callable[([str, str, int, int], List[str])]]=None, completer_method: Optional[Callable[([Any, str, str, int, int], List[str])]]=None, suppress_tab_hint: bool=False, descriptive_header: Optional[str]=None, **kwargs) -> argparse.Action:
    """
    Wrapper around _ActionsContainer.add_argument() which supports more settings used by thgcmd

    # Args from original function
    :param self: instance of the _ActionsContainer being added to
    :param args: arguments expected by argparse._ActionsContainer.add_argument

    # Customized arguments from original function
    :param nargs: extends argparse nargs functionality by allowing tuples which specify a range (min, max)
                  to specify a max value with no upper bound, use a 1-item tuple (min,)

    # Added args used by AutoCompleter
    :param choices_function: function that provides choices for this argument
    :param choices_method: thgcmd-app method that provides choices for this argument
    :param completer_function: tab-completion function that provides choices for this argument
    :param completer_method: thgcmd-app tab-completion method that provides choices for this argument
    :param suppress_tab_hint: when AutoCompleter has no results to show during tab completion, it displays the current
                              argument's help text as a hint. Set this to True to suppress the hint. If this argument's
                              help text is set to argparse.SUPPRESS, then tab hints will not display regardless of the
                              value passed for suppress_tab_hint. Defaults to False.
    :param descriptive_header: if the provided choices are CompletionItems, then this header will display
                               during tab completion. Defaults to None.

    # Args from original function
    :param kwargs: keyword-arguments recognized by argparse._ActionsContainer.add_argument

    Note: You can only use 1 of the following in your argument:
          choices, choices_function, choices_method, completer_function, completer_method

          See the header of this file for more information

    :return: the created argument action
    """
    nargs_range = None
    if nargs is not None:
        if isinstance(nargs, tuple):
            if len(nargs) == 1:
                nargs = (
                 nargs[0], INFINITY)
            elif not len(nargs) != 2:
                if not (isinstance(nargs[0], int) and isinstance(nargs[1], int) or nargs[1] == INFINITY):
                    raise ValueError('Ranged values for nargs must be a tuple of 1 or 2 integers')
            else:
                if nargs[0] >= nargs[1]:
                    raise ValueError('Invalid nargs range. The first value must be less than the second')
                if nargs[0] < 0:
                    raise ValueError('Negative numbers are invalid for nargs range')
                nargs_range = nargs
                range_min = nargs_range[0]
                range_max = nargs_range[1]
                if range_min == 0:
                    if range_max == 1:
                        nargs_adjusted = argparse.OPTIONAL
                        nargs_range = None
                    else:
                        nargs_adjusted = argparse.ZERO_OR_MORE
                        if range_max == INFINITY:
                            nargs_range = None
                else:
                    if range_min == 1 and range_max == INFINITY:
                        nargs_adjusted = argparse.ONE_OR_MORE
                        nargs_range = None
                    else:
                        nargs_adjusted = argparse.ONE_OR_MORE
        else:
            nargs_adjusted = nargs
        kwargs['nargs'] = nargs_adjusted
    new_arg = orig_actions_container_add_argument(self, *args, **kwargs)
    choice_params = [
     new_arg.choices, choices_function, choices_method, completer_function, completer_method]
    num_set = len(choice_params) - choice_params.count(None)
    if num_set > 1:
        err_msg = 'Only one of the following may be used in an argparser argument at a time:\nchoices, choices_function, choices_method, completer_function, completer_method'
        raise ValueError(err_msg)
    setattr(new_arg, ATTR_NARGS_RANGE, nargs_range)
    if choices_function:
        setattr(new_arg, ATTR_CHOICES_CALLABLE, ChoicesCallable(is_method=False, is_completer=False, to_call=choices_function))
    else:
        if choices_method:
            setattr(new_arg, ATTR_CHOICES_CALLABLE, ChoicesCallable(is_method=True, is_completer=False, to_call=choices_method))
        else:
            if completer_function:
                setattr(new_arg, ATTR_CHOICES_CALLABLE, ChoicesCallable(is_method=False, is_completer=True, to_call=completer_function))
            else:
                if completer_method:
                    setattr(new_arg, ATTR_CHOICES_CALLABLE, ChoicesCallable(is_method=True, is_completer=True, to_call=completer_method))
                setattr(new_arg, ATTR_SUPPRESS_TAB_HINT, suppress_tab_hint)
                setattr(new_arg, ATTR_DESCRIPTIVE_COMPLETION_HEADER, descriptive_header)
                return new_arg


argparse._ActionsContainer.add_argument = _add_argument_wrapper
orig_argument_parser_get_nargs_pattern = argparse.ArgumentParser._get_nargs_pattern

def _get_nargs_pattern_wrapper(self, action) -> str:
    nargs_range = getattr(action, ATTR_NARGS_RANGE, None)
    if nargs_range is not None:
        if nargs_range[1] == INFINITY:
            range_max = ''
        else:
            range_max = nargs_range[1]
        nargs_pattern = '(-*A{{{},{}}}-*)'.format(nargs_range[0], range_max)
        if action.option_strings:
            nargs_pattern = nargs_pattern.replace('-*', '')
            nargs_pattern = nargs_pattern.replace('-', '')
        return nargs_pattern
    return orig_argument_parser_get_nargs_pattern(self, action)


argparse.ArgumentParser._get_nargs_pattern = _get_nargs_pattern_wrapper
orig_argument_parser_match_argument = argparse.ArgumentParser._match_argument

def _match_argument_wrapper(self, action, arg_strings_pattern) -> int:
    nargs_pattern = self._get_nargs_pattern(action)
    match = re.match(nargs_pattern, arg_strings_pattern)
    if match is None:
        nargs_range = getattr(action, ATTR_NARGS_RANGE, None)
        if nargs_range is not None:
            raise ArgumentError(action, generate_range_error(nargs_range[0], nargs_range[1]))
    return orig_argument_parser_match_argument(self, action, arg_strings_pattern)


argparse.ArgumentParser._match_argument = _match_argument_wrapper

class Cmd2HelpFormatter(argparse.RawTextHelpFormatter):
    __doc__ = 'Custom help formatter to configure ordering of help text'

    def _format_usage(self, usage, actions, groups, prefix) -> str:
        if prefix is None:
            prefix = _('Usage: ')
        if usage is not None:
            usage %= dict(prog=(self._prog))
        else:
            if usage is None:
                usage = actions or '%(prog)s' % dict(prog=(self._prog))
            else:
                if usage is None:
                    prog = '%(prog)s' % dict(prog=(self._prog))
                    optionals = []
                    positionals = []
                    required_options = []
                    for action in actions:
                        if action.option_strings:
                            if action.required:
                                required_options.append(action)
                            else:
                                optionals.append(action)
                        else:
                            positionals.append(action)

                    format = self._format_actions_usage
                    action_usage = format(required_options + optionals + positionals, groups)
                    usage = ' '.join([s for s in [prog, action_usage] if s])
                    text_width = self._width - self._current_indent
                    if len(prefix) + len(usage) > text_width:
                        part_regexp = '\\(.*?\\)+|\\[.*?\\]+|\\S+'
                        req_usage = format(required_options, groups)
                        opt_usage = format(optionals, groups)
                        pos_usage = format(positionals, groups)
                        req_parts = re.findall(part_regexp, req_usage)
                        opt_parts = re.findall(part_regexp, opt_usage)
                        pos_parts = re.findall(part_regexp, pos_usage)
                        assert ' '.join(req_parts) == req_usage
                        assert ' '.join(opt_parts) == opt_usage
                        assert ' '.join(pos_parts) == pos_usage

                        def get_lines(parts, indent, prefix=None):
                            lines = []
                            line = []
                            if prefix is not None:
                                line_len = len(prefix) - 1
                            else:
                                line_len = len(indent) - 1
                            for part in parts:
                                if line_len + 1 + len(part) > text_width:
                                    if line:
                                        lines.append(indent + ' '.join(line))
                                        line = []
                                        line_len = len(indent) - 1
                                line.append(part)
                                line_len += len(part) + 1

                            if line:
                                lines.append(indent + ' '.join(line))
                            if prefix is not None:
                                lines[0] = lines[0][len(indent):]
                            return lines

                        if len(prefix) + len(prog) <= 0.75 * text_width:
                            indent = ' ' * (len(prefix) + len(prog) + 1)
                            if req_parts:
                                lines = get_lines([prog] + req_parts, indent, prefix)
                                lines.extend(get_lines(opt_parts, indent))
                                lines.extend(get_lines(pos_parts, indent))
                            else:
                                if opt_parts:
                                    lines = get_lines([prog] + opt_parts, indent, prefix)
                                    lines.extend(get_lines(pos_parts, indent))
                                else:
                                    if pos_parts:
                                        lines = get_lines([prog] + pos_parts, indent, prefix)
                                    else:
                                        lines = [
                                         prog]
                        else:
                            indent = ' ' * len(prefix)
                            parts = req_parts + opt_parts + pos_parts
                            lines = get_lines(parts, indent)
                            if len(lines) > 1:
                                lines = []
                                lines.extend(get_lines(req_parts, indent))
                                lines.extend(get_lines(opt_parts, indent))
                                lines.extend(get_lines(pos_parts, indent))
                            lines = [prog] + lines
                        usage = '\n'.join(lines)
                return '%s%s\n\n' % (prefix, usage)

    def _format_action_invocation(self, action) -> str:
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        parts = []
        if action.nargs == 0:
            parts.extend(action.option_strings)
            return ', '.join(parts)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string

    def _metavar_formatter(self, action, default_metavar) -> Callable:
        if action.metavar is not None:
            result = action.metavar
        else:
            if action.choices is not None:
                choice_strs = [str(choice) for choice in action.choices]
                result = '{%s}' % ', '.join(choice_strs)
            else:
                result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            return (result,) * tuple_size

        return format

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        nargs_range = getattr(action, ATTR_NARGS_RANGE, None)
        if nargs_range is not None:
            if nargs_range[1] == INFINITY:
                range_str = '{}+'.format(nargs_range[0])
            else:
                range_str = '{}..{}'.format(nargs_range[0], nargs_range[1])
            result = '{}{{{}}}'.format('%s' % get_metavar(1), range_str)
        else:
            if action.nargs == ZERO_OR_MORE:
                result = '[%s [...]]' % get_metavar(1)
            else:
                if action.nargs == ONE_OR_MORE:
                    result = '%s [...]' % get_metavar(1)
                else:
                    if isinstance(action.nargs, int) and action.nargs > 1:
                        result = '{}{{{}}}'.format('%s' % get_metavar(1), action.nargs)
                    else:
                        result = super()._format_args(action, default_metavar)
        return result


class ArgParser(argparse.ArgumentParser):
    __doc__ = 'Custom ArgumentParser class that improves error and help output'

    def __init__(self, *args, **kwargs):
        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = Cmd2HelpFormatter
        (super().__init__)(*args, **kwargs)

    def add_subparsers(self, **kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = 'sub-commands'
        return (super().add_subparsers)(**kwargs)

    def error(self, message: str) -> None:
        """Custom override that applies custom formatting to the error message"""
        lines = message.split('\n')
        linum = 0
        formatted_message = ''
        for line in lines:
            if linum == 0:
                formatted_message = 'Error: ' + line
            else:
                formatted_message += '\n       ' + line
            linum += 1

        self.print_usage(sys.stderr)
        formatted_message = style_error(formatted_message)
        self.exit(2, '{}\n\n'.format(formatted_message))

    def format_help(self) -> str:
        """Copy of format_help() from argparse.ArgumentParser with tweaks to separately display required parameters"""
        formatter = self._get_formatter()
        formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)
        formatter.add_text(self.description)
        for action_group in self._action_groups:
            if action_group.title == 'optional arguments':
                req_args = []
                opt_args = []
                for action in action_group._group_actions:
                    if action.required:
                        req_args.append(action)
                    else:
                        opt_args.append(action)

                formatter.start_section('required arguments')
                formatter.add_text(action_group.description)
                formatter.add_arguments(req_args)
                formatter.end_section()
                formatter.start_section(action_group.title)
                formatter.add_text(action_group.description)
                formatter.add_arguments(opt_args)
                formatter.end_section()
            else:
                formatter.start_section(action_group.title)
                formatter.add_text(action_group.description)
                formatter.add_arguments(action_group._group_actions)
                formatter.end_section()

        formatter.add_text(self.epilog)
        return formatter.format_help() + '\n'

    def _print_message(self, message, file=None):
        if message:
            if file is None:
                file = sys.stderr
            ansi_aware_write(file, message)