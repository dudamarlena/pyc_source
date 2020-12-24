# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tina/tina.py
# Compiled at: 2013-04-10 10:01:21
import optparse, os, sys
from tina_util import *

def handle_args():
    parser = optparse.OptionParser()
    parser.add_option('-c', '--commit', action='store_true', help='Commit changes to remotes (default: dry-run only)')
    parser.add_option('-i', '--interactive', action='store_true', help='Run in interactive mode')
    parser.add_option('-n', '--no-cleanup', action='store_true', help="Don't remove temporary files after committing")
    options, args = parser.parse_args()
    return options


def main():
    args = handle_args()
    if not args.commit or not os.path.exists('.tina'):
        checkout_and_parse('.', args.interactive)
    if args.commit:
        commit_and_push()
        if not args.no_cleanup:
            cleanup()
    else:
        print 'To commit these changes, re-run with --commit'


if __name__ == '__main__':
    main()