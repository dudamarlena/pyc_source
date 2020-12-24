# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/malicense/cmInterface.py
# Compiled at: 2018-03-25 02:42:27
# Size of source mod 2**32: 1948 bytes
""" inout.py: Command-line interfacing functions """
import argparse

def parseCmArgs():
    """ Parse command-line args specific for malicense

        Of course you can't give it a python package this way, just files

        Returns:
            (obj): processed arguments structure
    """
    parser = argparse.ArgumentParser(formatter_class=(argparse.RawTextHelpFormatter), description='Verify LICENSE files')
    parser.add_argument('licfile', type=(argparse.FileType('r')), help='The license file')
    parser.add_argument('snapfile', nargs='?', type=(argparse.FileType('rw')), default=None,
      help='The snapshot file')
    parser.add_argument('-s', '--snap', action='store_true', help='Make a snapshot')
    parser.add_argument('-q', '--quiet', action='store_true', help='Disable warning')
    parser.add_argument('-r', '--report-to', type=str, default=None, help='Address to send report. Example - 120.0.0.1:8000')
    args = parser.parse_args()
    args.licfilename = args.licfile.name
    del args.licfile
    if args.snapfile is not None:
        args.snapfilename = args.snapfile.name
    else:
        args.snapfilename = None
    del args.snapfile
    args.warnWith = None if args.quiet else print
    del args.quiet
    return args


def parseForServing():
    """ Parse command-line args specific for malicense-serve

        Returns:
            (obj): processed arguments structure
    """
    parser = argparse.ArgumentParser(formatter_class=(argparse.RawTextHelpFormatter), description='Serve LICENSE validity logger')
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument('-f', '--logfile', (argparse.FileType('rw')), default='report.txt')
    args = parser.parse_args()
    args.logfilename = args.logfile.name
    del args.logfile
    return args