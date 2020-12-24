# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/max/Workspace/snips/ProjectAliceModules/Tools/JsonValidator/src/Helpers.py
# Compiled at: 2019-11-21 04:18:12
# Size of source mod 2**32: 1480 bytes
import click

class OptionEatAll(click.Option):
    """OptionEatAll"""

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
            our_parser = parser._long_opt.get(name) or 
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break

        return retval