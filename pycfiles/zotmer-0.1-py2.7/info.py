# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/zotmer/commands/info.py
# Compiled at: 2016-12-21 18:11:04
"""
Usage:
    zot info <input>...
"""
from pykmer.container import probe
import docopt

def main(argv):
    opts = docopt.docopt(__doc__, argv)
    for inp in opts['<input>']:
        m, _ = probe(inp)
        print m


if __name__ == '__main__':
    main(sys.argv[1:])