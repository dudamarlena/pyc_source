# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/flask_proj/polarishub_flask/polarishub_flask/server/parser.py
# Compiled at: 2019-08-27 21:50:28
# Size of source mod 2**32: 494 bytes
import argparse, logging
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', help='Show all the logs in terminal.', action='store_true')
args = parser.parse_args()
verbose = args.verbose
if verbose:
    print('Running on verbose version.')
else:
    print('Running on quiet version.')
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
print('To open PolarisHub: http://localhost:5000/')

def printv(*args):
    if verbose:
        print(*args)