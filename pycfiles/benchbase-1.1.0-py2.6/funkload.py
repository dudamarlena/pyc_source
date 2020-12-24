# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/benchbase/funkload.py
# Compiled at: 2011-09-20 08:50:20
"""Extract information from an FunkLoad result file."""
from bencher import Bencher
from sqlitext import fl_label

class FunkLoad(Bencher):
    """FunkLoad importer / renderer"""
    _name = 'FunkLoad'
    _prefix = 'f_'
    _table = 'f_response'
    _cvus = 'cvus'

    def __init__(self, db, options):
        Bencher.__init__(self, db, options)

    def finalizeImport(self, bid, db):
        t = (
         bid,)
        db.execute('UPDATE f_response SET stamp = time WHERE stamp IS NULL AND bid = ?', t)
        db.execute("UPDATE f_response SET success = 1 WHERE result = 'Successful' AND success IS NULL AND bid = ?", t)
        db.execute('UPDATE f_response SET success = 0 WHERE success IS NULL AND bid = ?', t)
        c = self.db.cursor()
        c.execute('SELECT step, number, type, first(description) FROM f_response WHERE bid = ? GROUP BY step, number, type', t)
        for row in c:
            (step, number, rtype, description) = row
            label = fl_label(step, number, rtype, description)
            t = (label, bid, step, number, rtype)
            db.execute('UPDATE f_response SET lb = ? WHERE bid = ? AND step = ? AND number = ? AND type = ?', t)

    def _get_period_info_query(self):
        return ('SELECT COUNT(duration), AVG(duration), MAX(duration), MIN(duration), STDDEV(duration), MED(duration), P10(duration), P90(duration), P95(duration), P98(duration), TOTAL(duration), TOTAL(success) FROM {table} WHERE bid = ? AND stamp >= ? AND stamp < ?').format(table=self._table)

    def _get_interval_info(self):
        return ("SELECT time(interval(?, ?, stamp), 'unixepoch', 'localtime'), COUNT(duration), AVG(duration), MAX(duration), MIN(duration),  STDDEV(duration), MED(duration), P10(duration), P90(duration), P95(duration), P98(duration), TOTAL(duration), TOTAL(success),  AVG({cvus}) FROM {table} WHERE bid = ?").format(cvus=self._cvus, table=self._table)

    def _get_extra_info(self, bid, c=None):
        close_cursor = False
        if c is None:
            c = self.db.cursor()
            close_cursor = True
        ret = {}
        t = (
         bid,)
        c.execute('SELECT key, value FROM f_config WHERE bid = ?', t)
        for row in c:
            ret[row[0]] = row[1]

        if close_cursor:
            c.close()
        return ret