# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rcmp/main.py
# Compiled at: 2013-08-30 18:48:55
"""
Shell callable driver for the :py:mod:`rcmp` library.
"""
import argparse, fnmatch, logging, os, re, rcmp
__docformat__ = 'restructuredtext en'

def main():
    """
    Parses command line options and calls library.
    """
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    options = _parse_args()
    log_level = logging.ERROR
    if options.verbose == 1:
        log_level = rcmp.DIFFERENCES
    else:
        if options.verbose == 2:
            log_level = rcmp.SAMES
        else:
            if options.verbose == 3:
                log_level = rcmp.INDETERMINATES
            elif options.verbose > 3:
                log_level = logging.DEBUG
            logger.setLevel(log_level)
            logger.addHandler(handler)
            ignores = []
            for ifile in options.ignorefiles:
                if os.path.isfile(ifile):
                    with open(ifile, 'r') as (ignorefile):
                        ignores += [ line.strip() for line in ignorefile ]

        if options.crunch:
            ignores = rcmp.fntoreconcat(ignores)
        else:
            ignores = rcmp.fntore(ignores)
        result = rcmp.Comparison(lname=options.left, rname=options.right, ignores=ignores, exit_asap=options.exit_asap).cmp()
        if result == rcmp.Same:
            return 0
    return 1


def _parse_args():
    """
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description='Recursively CoMPares two trees.')
    parser.add_argument('left', help='First tree to check.')
    parser.add_argument('right', help='Second tree to check.')
    parser.add_argument('-e', '--exit-asap', '--exit-early', default=False, action='store_true', help='Exit on first difference. [default %(default)s]')
    parser.add_argument('-c', '--crunch', default=False, action='store_true', help='smash ignores into a single regexp [default %(default)s]')
    defaultignorefiles = [
     os.path.expanduser('.rcmpignore')]
    parser.add_argument('-i', '--ignorefile', action='append', type=str, default=defaultignorefiles, dest='ignorefiles', help="Read the named file as ignorefile. [default '%(default)s']")
    parser.add_argument('--no-ignores', action='store_const', dest='ignorefiles', const=[], help='reset the list of ignore files')
    parser.add_argument('-v', '--verbose', action='count', help='Be more verbose. (can be repeated)')
    return parser.parse_args()