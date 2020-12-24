# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/zotmer/commands/hist.py
# Compiled at: 2017-01-23 16:14:26
"""
Usage:
    zot hist <input>...

Options:
    -u              update the input container to include the histogram
"""
from pykmer.container import container
import docopt, sys

def main(argv):
    opts = docopt.docopt(__doc__, argv)
    for inp in opts['<input>']:
        with container(inp, 'r') as (z):
            if 'hist' in z.meta:
                h = z.meta['hist'].items()
                h.sort()
                for f, c in h:
                    print '%s\t%d\t%d' % (inp, f, c)


if __name__ == '__main__':
    main(sys.argv[1:])