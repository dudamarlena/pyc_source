# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/greg/Dropbox/code/dealertrack/flake8-diff/flake8diff/main.py
# Compiled at: 2015-07-13 15:56:52
"""
Run flake8 across a set of changed files and filter out violations occurring
only on the lines that were changed.

By default it's configured for "git diff master" which is useful for
buildmasters looking at a checked out PR.

To use, dump this in a file somewhere::

    $ pip install flake8-diff
    $ git checkout pr/NNN
    $ git merge origin/master
    $ flake8-diff

"""
from __future__ import print_function, unicode_literals
import argparse, logging, operator, os, six, sys
from .flake8 import COLORS, STRICT_MODES, Flake8Diff
from .vcs import SUPPORTED_VCS
LOGGING_FORMAT = b'%(asctime)-15s %(name)s %(levelname)s %(message)s'
ENVIRON_PREFIX = b'FLAKE8DIFF_{0}'
VERBOSITY_MAPPING = {0: logging.ERROR, 
   1: logging.INFO, 
   2: logging.DEBUG}
logging.basicConfig(format=LOGGING_FORMAT)
parser = argparse.ArgumentParser(description=b'This script runs flake8 across a set of changed files and filters out violations occurring only on the lines that were changed.')
parser.add_argument(b'commit', default=[
 b'origin/master'], nargs=b'*', type=six.text_type, help=b'At most two commit hashes or branch names which will be compared to figure out changed lines between the two. If only one commit is provided, that commit will be compared against current files.Default is "origin/master".')
parser.add_argument(b'--flake8-options', default=[], dest=b'flake8_options', metavar=b'<options>', nargs=argparse.REMAINDER, type=six.text_type, help=b'Options to be passed to flake8 command. Can be used to configure flake8 on-the-fly when flake8 configuration file is not present.')
parser.add_argument(b'--vcs', choices=list(map(operator.attrgetter(b'name'), SUPPORTED_VCS.values())), type=six.text_type, help=(b'VCS to use. By default VCS is attempted to determine automatically. Can be any of "{0}"').format((b', ').join(map(operator.attrgetter(b'name'), SUPPORTED_VCS.values()))))
parser.add_argument(b'--standard-flake8-output', action=b'store_true', default=False, dest=b'standard_flake8_output', help=b'Output standard flake8 output instead of simplified, more readable summary.')
parser.add_argument(b'-v', b'--verbose', action=b'count', default=0, help=b'Be verbose. This will print out every compared file. Can be supplied multiple times to increase verbosity level')
default_color = os.environ.get(ENVIRON_PREFIX.format(b'COLOR'), b'colorful')
parser.add_argument(b'--color', choices=COLORS.keys(), default=default_color, type=six.text_type, help=(b'Color theme to use. Default is "{0}". Can be any of "{1}"').format(default_color, (b', ').join(COLORS.keys())))
parser.add_argument(b'--strict-mode', choices=STRICT_MODES.keys(), default=b'only_lines', type=six.text_type, dest=b'strict_mode', help=(b'Strict mode to use on the files where violations are found. Default is "only_lines". Can be any of "{0}"').format((b', ').join(STRICT_MODES.keys())))

def main():
    args = parser.parse_args()
    if len(args.commit) > 2:
        parser.error(b'At most 2 commits can be provided.')
    options = {b'commits': args.commit, 
       b'vcs': args.vcs, 
       b'flake8_options': args.flake8_options, 
       b'standard_flake8_output': args.standard_flake8_output, 
       b'color_theme': args.color, 
       b'strict_mode': args.strict_mode}
    logging.getLogger(b'').setLevel(VERBOSITY_MAPPING.get(args.verbose, 0))
    any_violations = False
    try:
        any_violations = not Flake8Diff(commits=args.commit, options=options).process()
    except Exception as e:
        parser.error(six.text_type(e))

    if any_violations:
        sys.exit(1)