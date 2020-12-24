# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argsimple/help.py
# Compiled at: 2020-04-26 21:06:40
# Size of source mod 2**32: 4561 bytes
import sys
from collections import OrderedDict
from typing import Dict, List
from .option import Option

class Help:
    formatter = None

    @classmethod
    def show_and_exit(cls, options: Option, program: str='', version: str='', docstring: str='', epilogue: str='') -> None:
        if cls.formatter is None:
            cls.formatter = DefaultHelpFormatter(options, program, version, docstring, epilogue)
        help_str = cls.formatter.help_string()
        print(help_str)
        sys.exit(0)

    @classmethod
    def usage(cls, options: Option, program: str='') -> None:
        if cls.formatter:
            formatter = cls.formatter
        else:
            formatter = DefaultHelpFormatter(options, program)
        usage_str = formatter.usage_string()
        print(usage_str)


class DefaultHelpFormatter:
    indent = 2

    def __init__(self, options: Option, program: str='', version: str='', docstring: str='', epilogue: str=''):
        self.options = options
        self.program = program
        self.version = version
        self.docstring = docstring
        self.epilogue = epilogue

    def help_string(self) -> str:
        help_str = ''
        self._send_help_to_last()
        usage = self.usage_string()
        groups = self._group_options()
        widths = self._column_widths()
        opt_str = self._to_string(groups, widths)
        if usage:
            help_str += f"\n{usage}"
        if self.docstring:
            help_str += f"\n\n{self.docstring}"
        if opt_str:
            help_str += f"\n{opt_str}"
        if self.epilogue:
            help_str += f"\n\n{self.epilogue}"
        help_str += '\n'
        return help_str

    def usage_string(self) -> str:
        required = []
        for option in self.options:
            if option.required:
                short = option.prefixes[0]
                metavar = option.metavar
                if metavar:
                    prefix_string = f"{short} {metavar}"
                else:
                    prefix_string = short
                required.append(prefix_string)

        required_str = ' '.join(required)
        usage = f"Usage: {self.program} [options] {required_str}"
        return usage

    def _send_help_to_last(self) -> List[Option]:
        new_opt = []
        help_opt = []
        for option in self.options:
            if option.action == 'help':
                help_opt.append(option)
            else:
                new_opt.append(option)

        self.options = new_opt + help_opt
        return self.options

    def _group_options(self) -> Dict[(str, List[Option])]:
        groups = OrderedDict()
        for option in self.options:
            if option.group:
                groups.setdefault(option.group, []).append(option)

        for option in self.options:
            if option.group or option.required:
                groups.setdefault('required argments', []).append(option)

        for option in self.options:
            if not option.group:
                option.required or groups.setdefault('optional arguments', []).append(option)

        return groups

    def _column_widths(self) -> List[int]:
        widths = [0, 0]
        line_tuples = []
        for option in self.options:
            prfx_str = ', '.join(option.prefixes)
            help_str = option.help
            line_tuples.append((prfx_str, help_str))

        if line_tuples:
            widths[0] = max([len(i[0]) for i in line_tuples])
            widths[1] = max([len(i[1]) for i in line_tuples])
        return widths

    def _to_string(self, groups, widths) -> str:
        lines = []
        for group, options in groups.items():
            lines.append('')
            lines.append(group + ':')
            for option in options:
                prfx_str = ', '.join(option.prefixes)
                help_str = option.help
                prfx_str += ' ' * (widths[0] - len(prfx_str))
                help_str += ' ' * (widths[1] - len(help_str))
                lines.append(f"{' ' * self.indent}{prfx_str}   {help_str}")

        return '\n'.join(lines)