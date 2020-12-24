# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/benchbase/sar.py
# Compiled at: 2011-09-15 17:15:00
"""Extract information from a sysstat sar text file."""
import logging
from util import mygzip

class Sar(object):
    """Handle sysstat sar file."""

    def __init__(self, db, options):
        self.options = options
        self.db = db

    def doImport(self, bid, filename):
        c = self.db.cursor()
        options = self.options
        host = options.host
        t = (bid, host, options.comment)
        logging.info('Importing sar file %s into bid: %s' % (filename, bid))
        c.execute('INSERT INTO host (bid, host, comment) VALUES (?, ?, ?)', t)
        if filename.endswith('.gz'):
            f = mygzip(filename)
        else:
            f = open(filename)
        in_cpu = False
        in_disk = False
        count = 0
        while True:
            line = f.readline()
            if not line:
                break
            if 'CPU      %usr' in line:
                in_cpu = True
                continue
            if 'DEV       tps' in line:
                in_disk = True
                continue
            if in_cpu:
                if 'all' not in line:
                    continue
                if 'Average' in line:
                    in_cpu = False
                    continue
                t = [
                 bid, host] + line.split()
                t.remove('all')
                c.execute('INSERT INTO cpu (bid, host, date, usr, nice, sys, iowait, steal, irq, soft, guest, idle) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', t)
                count += 1
            elif in_disk:
                if 'Average' in line:
                    in_disk = False
                    break
                r = line.split()
                t = [bid, host, r[0], r[1], r[2], r[3], r[4], r[9]]
                c.execute('INSERT INTO disk (bid, host, date, dev, tps, rd_sec_per_s, wr_sec_per_s, util) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', t)
                count += 1

        c.close()
        self.db.commit()
        logging.info('%d lines imported.' % count)

    def getInfo(self, bid):
        t = (
         bid,)
        c = self.db.cursor()
        c.execute('SELECT host, comment FROM host WHERE bid = ?', t)
        ret = {'sar': {}}
        for (host, comment) in c:
            ret['sar'][host] = comment

        return ret