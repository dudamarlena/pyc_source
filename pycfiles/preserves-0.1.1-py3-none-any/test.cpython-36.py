# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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