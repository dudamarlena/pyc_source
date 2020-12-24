# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/app/lbsramtransfert.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 1133 bytes
import logging, sys, argparse
logging.basicConfig()
_logger = logging.getLogger(__name__)

def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all',
      dest='all',
      action='store_true',
      default=False,
      help='Transfert all scans found, even the unfinished one')
    parser.add_argument('--delete-aborted',
      dest='delete_aborted',
      action='store_true',
      default=False,
      help='Remove aborted scans (both in lbsram and rnice if any found)')
    parser.add_argument('--loop',
      dest='looping',
      action='store_true',
      default=False,
      help='detection loop on the root folder until stopped')
    parser.add_argument('-r',
      '--root', default='/lbsram',
      help='Define the root directory where to look for scans')
    options = parser.parse_args(argv[1:])


if __name__ == '__main__':
    main(sys.argv)