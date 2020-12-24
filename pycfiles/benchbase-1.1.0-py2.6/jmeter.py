# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/benchbase/jmeter.py
# Compiled at: 2011-09-20 08:24:55
"""Extract information from an JMeter result file."""
import logging, csv
from bencher import Bencher
from util import mygzip
CSV_COLS = {10: [
      'ts', 't', 'lb', 'tn', 'de', 's', 'by', 'ng', 'na', 'lt'], 
   12: [
      'ts', 't', 'lb', 'rc', 'rm', 'tn', 'de', 's', 'by', 'ng', 'na', 'lt']}

class JMeter(Bencher):
    """JMeter importer / renderer"""
    _name = 'JMeter'
    _prefix = 'j_'
    _table = 'j_sample'
    _cvus = 'na'

    def __init__(self, db, options):
        Bencher.__init__(self, db, options)

    def importOtherFormat(self, bid, filename):
        """Handle CSV file"""
        db = self.db
        if filename.endswith('.gz'):
            f = mygzip(filename)
        else:
            f = open(filename)
        jtlReader = csv.reader(f)
        count = 0
        error = 0
        insert_query = None
        for row in jtlReader:
            row = [ unicode(cell, 'utf-8').encode('ascii', 'ignore') for cell in row ]
            if insert_query is None:
                if len(row) not in CSV_COLS.keys():
                    raise ValueError('Unsupported format')
                values = ('?, ' * (len(row) + 1))[:-2]
                insert_query = 'INSERT INTO j_sample (bid, ' + (', ').join(CSV_COLS[len(row)]) + ') VALUES (' + values + ')'
            try:
                db.execute(insert_query, [bid] + row)
                count += 1
            except Exception, e:
                logging.warning(e)
                error += 1
                print 'x',

        db.commit()
        logging.info('%i samples imported, %i error(s).' % (count, error))
        return

    def finalizeImport(self, bid, db):
        db.execute('UPDATE j_sample SET stamp = ts/1000 WHERE stamp IS NULL;')
        db.execute("UPDATE j_sample SET success = 1 WHERE s IN ('true', 'TRUE', 'True') AND success IS NULL;")
        db.execute("UPDATE j_sample SET success = 0 WHERE s NOT IN ('true', 'TRUE', 'True') AND success IS NULL;")

    def _get_period_info_query(self):
        return ('SELECT COUNT(t), AVG(t)/1000., MAX(t)/1000., MIN(t)/1000.,  STDDEV(t)/1000.,  MED(t)/1000., P10(t)/1000, P90(t)/1000., P95(t)/1000., P98(t)/1000., TOTAL(t)/1000., TOTAL(success) FROM {table} WHERE bid = ? AND stamp >= ? AND stamp < ?').format(table=self._table)

    def _get_interval_info(self):
        return ("SELECT time(interval(?, ?, stamp), 'unixepoch', 'localtime'), COUNT(t), AVG(t)/1000., MAX(t)/1000., MIN(t)/1000.,  STDDEV(t)/1000.,   MED(t)/1000., P10(t)/1000., P90(t)/1000., P95(t)/1000., P98(t)/1000., TOTAL(t)/1000., TOTAL(success),  AVG({cvus}) FROM {table} WHERE bid = ?").format(cvus=self._cvus, table=self._table)