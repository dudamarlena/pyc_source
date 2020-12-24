# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/presenzialo.py
# Compiled at: 2020-01-27 05:59:20
# Size of source mod 2**32: 1231 bytes
import datetime, argparse
from .presenzialo_web import PRweb
from .presenzialo_day import PRday, add_parser_date
from .presenzialo_args import add_parser_debug
from .presenzialo_address import PRaddress, add_parser_address
from .presenzialo_auth import PRauth, add_parser_auth

def presenzialo(args):
    pr_auth = PRauth(**vars(args))
    pr_web = PRweb(pr_auth)
    if args.workers is not None or args.phones is not None or args.cache_address:
        address = PRaddress(pr_web, args.cache_address, args.raw)
        if args.workers:
            address.present(args.workers)
            print(address)
        if args.phones:
            address.phone(args.phones)
            print(address)
    else:
        pr_day = PRday(pr_web.timecard(args.day_from, args.day_to))
        for d in pr_day.days:
            print(d)


def main():
    parser = argparse.ArgumentParser(prog='presenzialo',
      description='presenzialo',
      formatter_class=(argparse.RawDescriptionHelpFormatter))
    add_parser_debug(parser)
    add_parser_date(parser)
    add_parser_address(parser)
    add_parser_auth(parser)
    args = parser.parse_args()
    presenzialo(args)


if __name__ == '__main__':
    main()