# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/cctagutils/cli.py
# Compiled at: 2007-03-15 10:29:40
__doc__ = '\ncli.py\n\nSupport structures for command line interface to tagging, embedding\nand lookup.\n'
__id__ = '$Id: cli.py 700 2007-02-13 12:56:09Z nyergler $'
__version__ = '$Revision: 700 $'
__copyright__ = '(c) 2004, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'
import optparse

def expandFiles(args):
    """Expands any file wildcards contained in args and returns an expanded,
    explicit list.
    """
    return args


class Option(optparse.Option):
    __module__ = __name__
    ATTRS = optparse.Option.ATTRS + ['required']

    def _check_required(self):
        if self.required and not self.takes_value():
            raise optparse.OptionError("required flag set for option that doesn't take a value", self)

    CHECK_METHODS = optparse.Option.CHECK_METHODS + [_check_required]

    def process(self, opt, value, values, parser):
        optparse.Option.process(self, opt, value, values, parser)
        parser.option_seen[self] = 1


class OptionParser(optparse.OptionParser):
    __module__ = __name__

    def _init_parsing_state(self):
        optparse.OptionParser._init_parsing_state(self)
        self.option_seen = {}

    def check_values(self, values, args):
        for option in self.option_list:
            if isinstance(option, Option) and option.required and not self.option_seen.has_key(option):
                self.error('%s not supplied' % option)

        return (
         values, args)