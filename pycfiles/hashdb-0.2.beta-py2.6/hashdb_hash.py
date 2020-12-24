# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hashdb/hashdb_hash.py
# Compiled at: 2011-01-06 01:19:27
from hashdb_output import log, isatty
import hashdb_onsigint, hashdb_progress, hashlib, sys

def build_hash(target, width=None):
    hasher = hashlib.md5()
    if target.stat.st_size == 0:
        return 'd41d8cd98f00b204e9800998ecf8427e'
    else:
        display = log.is_verbose and isatty(sys.stdout) and target.stat.st_size > 1048576
        if display:
            if width == None:
                width = hashdb_progress.find_terminal_width()
            total = 0
        try:
            if display:
                print '\x1b[?25l\r',
                print hashdb_progress.build_progress(total, target.stat.st_size, width) + '\r',
            with open(target.true, 'rb') as (f):
                while True:
                    data = f.read(131072)
                    if not data:
                        break
                    hasher.update(data)
                    if display:
                        total += len(data)
                        print hashdb_progress.build_progress(total, target.stat.st_size, width) + '\r',

            if display:
                print hashdb_progress.build_progress(target.stat.st_size, target.stat.st_size, width) + '\r',
                print '\x1b[?25h'
            return hasher.hexdigest()
        except OSError, ex:
            log.warning('warning: Unable to hash file %r: %s' % (target.user, ex))
        except IOError, ex:
            log.warning('warning: Unable to hash file %r: %s' % (target.user, ex))

        return


if __name__ == '__main__':
    import hashdb_walk
    w = hashdb_walk.Walker()
    w.add_target('test/Burn.Notice.S04E18.Last.Stand.HDTV.XviD-FQM.[VTV].avi')
    hash = build_hash(w._targets[0])
    print '\x1b[0K' + hash + '  %s' % w._targets[0].user