# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lumpy/cli.py
# Compiled at: 2016-07-22 19:41:43
import argparse, logging
from .mail import Mail

def parse():
    parser = argparse.ArgumentParser(prog='lumpy', description=Mail.send.__doc__)
    arg = parser.add_argument
    arg('--from', '-f', nargs='?', dest='sender')
    arg('recipient', metavar='recipient@example.com')
    arg('--subject', '-s', nargs='?')
    arg('--body', '-b', nargs='?')
    arg('--port', '-p', nargs='?')
    arg('--content-type', '-c', nargs='?')
    arg('--mxrecords', '--mx', '-m', nargs='*', help='List of whitespace-separated mx records')
    arg('--verbose', '-v', action='store_true')
    return parser.parse_args()


def run():
    args = parse()
    if args.verbose:
        logging.root.level = logging.INFO
    del args.verbose
    mail_args = {k:v for k, v in args.__dict__.items() if v if v}
    Mail(**mail_args).send()