# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/zotmer/commands/dump.py
# Compiled at: 2017-01-23 16:14:26
"""
Usage:
    zot dump <input>
"""
from pykmer.basics import render
from pykmer.container import container
from pykmer.container.std import readKmers, readKmersAndCounts
import docopt, sys

def main(argv):
    opts = docopt.docopt(__doc__, argv)
    inp = opts['<input>']
    with container(inp, 'r') as (z):
        K = z.meta['K']
        if 'kmers' not in z.meta:
            print >> sys.stderr, 'cannot dump "%s" as it contains no k-mers' % (inp,)
            return
        if 'counts' in z.meta:
            xs = readKmersAndCounts(z)
            for x, c in xs:
                print '%s\t%d' % (render(K, x), c)

        else:
            xs = readKmers(z)
            for x in xs:
                print render(K, x)


if __name__ == '__main__':
    main(sys.argv[1:])