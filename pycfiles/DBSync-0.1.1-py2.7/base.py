# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dbsync/syncs/base.py
# Compiled at: 2015-04-10 05:21:53
__author__ = 'nathan'
import threading, logging, time, codecs

class BaseSync:

    def __init__(self):
        pass

    def run(self):
        pass


class Dumper(threading.Thread):

    def __init__(self, dst_file, sq):
        threading.Thread.__init__(self)
        self._logger = logging.getLogger('dbsync.syncs')
        self.dst_file = dst_file
        self.sq = sq

    def run(self):
        start = time.clock()
        count = 0
        self._logger.info('run start')
        with codecs.open(self.dst_file, 'w', 'utf-8') as (w):
            for item in self.sq.naive().iterator():
                w.write(item.unicode_dumps() + '\n')
                count += 1

        self._logger.info('write count : %d' % count)
        end = time.clock()
        self._logger.info('%s file count %d, run time : %.03f seconds' % (self.dst_file, count, end - start))

    def stop(self):
        self.thread_stop = True