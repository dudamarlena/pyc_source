# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/Workspace/snips/ProjectAliceModules/Tools/JsonValidator/src/Helpers.py
# Compiled at: 2019-11-21 04:18:12
# Size of source mod 2**32: 1480 bytes
import click

class OptionEatAll(click.Option):
    __doc__ = '\n\ttaken from https://stackoverflow.com/questions/48391777/nargs-equivalent-for-options-in-click\n\t'

    def __init__(self, *args, **kwargs):
        self.save_other_options = kwargs.pop('save_other_options', True)
        nargs = kwargs.pop('nargs', -1)
        assert nargs == -1, f"nargs, if set, must be -1 not {nargs}"
        (super(OptionEatAll, self).__init__)(*args, **kwargs)
        self._previous_parser_process = None
        self._eat_all_parser = None

    def add_to_parser(self, parser, ctx):

        def parser_process(value, state):
            done = False
            value = [value]
            if self.save_other_options:
                while state.rargs and not done:
                    for prefix in self._eat_all_parser.prefixes:
                        if state.rargs[0].startswith(prefix):
                            done = True

                    done or value.append(state.rargs.pop(0))

            else:
                value += state.rargs
                state.rargs[:] = []
            value = tuple(value)
            self._previous_parser_process(value, state)

        retval = super(OptionEatAll, self).add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break

        return retval