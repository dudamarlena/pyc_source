# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/_utils/custom_options/option_nargs.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 1956 bytes
"""
Custom Click options for multiple arguments
"""
import click

class OptionNargs(click.Option):
    __doc__ = '\n    A custom option class that allows parsing for multiple arguments\n    for an option, when the number of arguments for an option are unknown.\n    '

    def __init__(self, *args, **kwargs):
        self.nargs = kwargs.pop('nargs', -1)
        (super(OptionNargs, self).__init__)(*args, **kwargs)
        self._previous_parser_process = None
        self._nargs_parser = None

    def add_to_parser(self, parser, ctx):

        def parser_process(value, state):
            next_option = False
            value = [value]
            while state.rargs and not next_option:
                for prefix in self._nargs_parser.prefixes:
                    if state.rargs[0].startswith(prefix):
                        next_option = True

                next_option or value.append(state.rargs.pop(0))

            value = tuple(value)
            self._previous_parser_process(value, state)

        super(OptionNargs, self).add_to_parser(parser, ctx)
        for name in self.opts:
            option_parser = getattr(parser, '_long_opt').get(name) or getattr(parser, '_short_opt').get(name)
            if option_parser:
                self._nargs_parser = option_parser
                self._previous_parser_process = option_parser.process
                option_parser.process = parser_process
                break