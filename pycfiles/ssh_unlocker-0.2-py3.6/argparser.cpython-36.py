# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/unlocker/argparser.py
# Compiled at: 2017-10-09 13:30:30
# Size of source mod 2**32: 642 bytes
import argparse
parser = argparse.ArgumentParser(description='\n    Cryptsetup SSH server unlocker.\n    This utility is repeatedly polling configured servers and tries to unlock the encrypted root partition using cryptsetup once the SSH connection is available.\n')
parser.add_argument('-c', '--config', required=False, default='config.ini', help='Path to config file - defaults to config.ini')
parser.add_argument('-v', '--verbose', required=False, action='store_true', help='Increase verbosity level to DEBUG')
parser.add_argument('--logfile', required=False, help='Path to log file. By default the log messages are printed to stderr')