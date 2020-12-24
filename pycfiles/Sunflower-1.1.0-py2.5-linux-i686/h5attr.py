# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sunflower/h5attr.py
# Compiled at: 2009-01-12 20:14:59
from __future__ import division, with_statement
__version__ = '$Revision: 192 $'
import sys
from .hdf5 import h5open
from ._utils import progress

def h5attr(h5filenames, set_attrs):
    for h5filename in h5filenames:
        progress(h5filename)
        with h5open(h5filename, 'r+') as (h5file):
            for leaf in h5file.walkNodes(classname='Leaf'):
                for (key, value) in set_attrs.iteritems():
                    setattr(leaf.attrs, key, value)


def parse_options(args):
    from ._optparse import OptionParser
    usage = '%prog [OPTION]... FILE...'
    version = '%%prog %s' % __version__
    parser = OptionParser(usage=usage, version=version)
    parser.add_option('-s', '--set-str', action='update', dest='set_attrs', default={}, metavar='KEY VALUE', help='set KEY=VALUE')
    parser.add_option('-i', '--set-int', action='update', type=int, dest='set_attrs', metavar='KEY VALUE', help='set KEY=VALUE')
    (options, args) = parser.parse_args(args)
    if not len(args) >= 1:
        parser.print_usage()
        sys.exit(1)
    return (options, args)


def main(args=sys.argv[1:]):
    (options, args) = parse_options(args)
    return h5attr(args, options.set_attrs)


if __name__ == '__main__':
    sys.exit(main())