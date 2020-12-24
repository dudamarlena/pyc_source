# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2ladderMgmt\__main__.py
# Compiled at: 2018-08-21 11:19:17
# Size of source mod 2**32: 2497 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from sc2ladderMgmt import addLadder, getLadder, delLadder, getKnownLadders, __version__
from argparse import ArgumentParser
import os
if __name__ == '__main__':
    defs = getKnownLadders()
    ALLOWED_LADDERS = list(defs)
    description = 'Available valid ladder values for NAME:%s    %s' % (os.linesep, ('%s    ' % os.linesep).join(ALLOWED_LADDERS))
    parser = ArgumentParser(description=description, epilog=('version: %s' % __version__.__version__))
    optionsLadderOps = parser.add_argument_group('ladder operations')
    optionsLadderOps.add_argument('--add', action='store_true', help="Add a new ladder definition from provided criterira values. ('name' is required; see criteria definition below).")
    optionsLadderOps.add_argument('--get', type=str, help='the name of the ladder to use.', metavar='NAME')
    optionsLadderOps.add_argument('--rm', type=str, help='the name of the ladder to remove.', metavar=' NAME')
    optionsCriteria = parser.add_argument_group('critiera used when --add')
    optionsCriteria.add_argument('criteria', nargs='*', help='remaining arguments for the specified action.')
    options = parser.parse_args()
    if options.add:
        terms = [a.split('=') for a in options.criteria]
        kwargs = {}
        try:
            for i, (k, v) in enumerate(terms):
                kwargs[k] = v

            print(addLadder(kwargs))
        except ValueError:
            print("ERROR: key '%s' must specify a value using '=' followed by a value (no whitespace)." % terms[i][0])

    else:
        if options.get:
            print(getLadder(options.get))
        else:
            if options.rm:
                print(delLadder(options.rm))
            else:
                for ladder in defs.values():
                    print('object:', ladder)
                    for k, v in ladder.attrs.items():
                        print('%24s : %s' % (k, v))

                if defs:
                    print('Found %d ladder definition(s)' % len(defs))
                else:
                    print('No ladder definitions are available.')