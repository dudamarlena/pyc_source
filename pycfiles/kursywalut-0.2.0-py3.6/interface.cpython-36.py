# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kursywalut/interface/interface.py
# Compiled at: 2018-12-20 11:59:26
# Size of source mod 2**32: 2082 bytes
"""Interface module.

Simple CLI interface to run the program.

"""
import logging
from ..funcs.string_operations import print_unicode
from .. import version
from ..handlers import MoneyPlHandler
logger = logging.getLogger(__name__)

class Config(object):
    __doc__ = 'Class for program configuration data.\n\n    Attributes:\n        opts: sys.args passed while running the program\n\n    '
    opts = None


def get_moneypl():
    """Get money.pl currency data.

    Returns:
        OrderedDict: Parsed data.

    """
    print_unicode('Getting data from website.')
    mpl = MoneyPlHandler()
    data = mpl.get_moneypl()
    print_unicode('data download time: {}'.format(mpl.download_time))
    print_unicode('parse time: {}'.format(mpl.parse_time))
    return data


def pretty_print_data(data):
    """Format received data.

    Args:
        data (ordereddict): OrderedDict to be printed.

    """
    detail_str = ''
    for key, value in data.items():
        if key == 'FOREX':
            print_unicode(key + '\tkupno\tsprzedaż\n')
        else:
            if key == 'NBP':
                print_unicode(key + '\tkurs średni\n')
        for name, detail in value.items():
            if type(detail) == list:
                for item in detail:
                    detail_str = detail_str + '\t' + item

            else:
                detail_str = detail
            if name == 'DATA':
                tab = '\t'
            else:
                tab = ''
            if key == 'FOREX':
                print_unicode(name + '{}'.format(tab) + detail_str)
            else:
                if key == 'NBP':
                    print_unicode(name + '\t' + detail_str)
            detail_str = ''

        print_unicode('')


def display_header():
    """Display header."""
    print_unicode('##################')
    print_unicode('$ KursyWalut ' + version.__version__ + ' $')
    print_unicode('##################\n')


def run(*args):
    """Run the program."""
    Config.opts = args
    display_header()
    data = get_moneypl()
    print_unicode('')
    pretty_print_data(data)