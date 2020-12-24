# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/MacDev/perso/atomisator.ziade.org/packages/pbp.scripts/pbp/scripts/hotshot2dot.py
# Compiled at: 2008-08-25 04:58:53
import sys, os, hotshot.stats
from pbp.scripts.gprof2dot import run_script

def main():
    if len(sys.argv) != 2:
        print 'Usage: %s HOTSHOT_FILE' % sys.argv[0]
        sys.exit(0)
    filename = sys.argv[1]
    s = hotshot.stats.load(filename)
    pstats = filename + '.pstats'
    s.dump_stats(pstats)
    try:
        sys.argv = [
         sys.argv[0], '-f', 'pstats', pstats]
        run_script()
    finally:
        os.remove(pstats)


if __name__ == '__main__':
    main()