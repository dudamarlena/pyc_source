# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/__init__.py
# Compiled at: 2019-07-17 15:13:04
# Size of source mod 2**32: 639 bytes
"""This simply imports certain things for backwards compatibility."""
from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass

from .ansi import style
from .argparse_custom import ArgParser, CompletionItem
from .thgcmd import Cmd, Statement, EmptyStatement, categorize
from .thgcmd import with_argument_list, with_argparser, with_argparser_and_unknown_args, with_category
from .constants import DEFAULT_SHORTCUTS
from .pyscript_bridge import CommandResult