# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/test.py
# Compiled at: 2020-01-24 05:44:53
# Size of source mod 2**32: 1019 bytes
import datetime, argparse
from .presenzialo_web import PRweb
from .presenzialo_day import PRday, add_parser_date
from .presenzialo_args import add_parser_debug
from .presenzialo_address import PRaddress, add_parser_address
from .presenzialo_auth import PRauth, add_parser_auth
from .presenzialo_auth import PRauth, config_auth
from .presenzialo_web import PRweb
from .presenzialo_day import PRday

def main():
    parser = argparse.ArgumentParser(prog='presenzialo',
      description='presenzialo',
      formatter_class=(argparse.RawDescriptionHelpFormatter))
    add_parser_debug(parser)
    add_parser_date(parser)
    add_parser_address(parser)
    add_parser_auth(parser)
    args = parser.parse_args()
    print(args)
    pr_auth = PRauth(**vars(args))
    pr_web = PRweb(pr_auth)
    pr_day = PRday(pr_web.timecard())
    print(pr_day.days)


if __name__ == '__main__':
    main()