# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sunflower/driver/sql.py
# Compiled at: 2009-01-12 20:14:59
from __future__ import division
__version__ = '$Revision: 366 $'
from itertools import izip
import re, sys
from warnings import filterwarnings
from MySQLdb import IntegrityError
from dboptions import DbOptionParser, connect
import docsql
from numpy import empty, uint8
from . import Driver, DriverHelpFormatter, defline_identifier
QUANTIZATION_SCALE = 255.0

class Insert_tf(docsql.Insert):
    """
    INSERT INTO tf SET name=%s
    """
    pass


class Select_tf_id(docsql.SelectOneCell):
    """
    SELECT tf_id FROM tf WHERE name=%s
    """
    pass


class Insert_seq_region(docsql.Insert):
    """
    INSERT INTO seq_region SET name=%s
    """
    pass


class Select_seq_region_id(docsql.SelectOneCell):
    """
    SELECT seq_region_id FROM seq_region WHERE name=%s
    """
    pass


class Insert_prob(docsql.Insert):
    """
    INSERT DELAYED INTO prob (tf_id, seq_region_id, seq_region_start,
                              seq_region_end, probs)
    VALUES (%s, %s, %s, %s, %s)
    """
    pass


def get_rowid(insert, select, name, connection):
    try:
        cursor = insert(name, connection=connection)
        return cursor.lastrowid
    except IntegrityError:
        return select(name, connection=connection)


class RowAppender(object):
    """
    converts 0-based to offset 1-based and appends
    """

    def __init__(self, sequence, tf_id, seq_region_id, start):
        self.sequence = sequence
        self.tf_id = tf_id
        self.seq_region_id = seq_region_id
        self.start = start

    def __call__(self, start, end, values):
        self.sequence.append([self.tf_id,
         self.seq_region_id,
         start + self.start,
         end + self.start - 1,
         values])


re_charrun = re.compile('(.)\\1{17,}')

class SQLDriver(Driver):

    def __init__(self, command_args, *args, **kwargs):
        (options, command_args) = self.parse_options(command_args)
        self.dboptions = options.dboptions
        Driver.__init__(self, [], *args, **kwargs)

    @staticmethod
    def get_option_parser():
        usage = '%prog --driver=DRIVER [OPTION...] MODEL SEQFILE [DRIVEROPTION...]'
        return DbOptionParser(usage=usage, formatter=DriverHelpFormatter())

    def parse_options(self, args):
        parser = self.get_option_parser()
        (options, args) = parser.parse_args(args)
        if len(args) != 0:
            self.print_usage()
            sys.exit(1)
        return (options, args)

    def __enter__(self):
        connection = connect(self.dboptions)
        self.connection = connection
        self.tf_ids = [ get_rowid(Insert_tf, Select_tf_id, colname, connection) for colname in self.colnames
                      ]
        return self

    def __exit__(self, *exc_info):
        self.connection.close()

    def __call__(self, arr, (defline, seq)):
        name = defline_identifier(defline)
        connection = self.connection
        seq_region_id = get_rowid(Insert_seq_region, Select_seq_region_id, name, connection=connection)
        start = self.defline_start(defline)
        assert start >= 1
        quantized_array = (arr * QUANTIZATION_SCALE).astype(uint8)
        rows = []
        for (tf_id, tf_vec) in izip(self.tf_ids, quantized_array.T):
            values = tf_vec.tostring()
            appender = RowAppender(rows, tf_id, seq_region_id, start)
            charrun_start = None
            charrun_end = 0
            for m_charrun in re_charrun.finditer(values):
                charrun_start = m_charrun.start()
                if charrun_start != charrun_end:
                    values_chunk = values[charrun_end:charrun_start]
                    appender(charrun_end, charrun_start, values_chunk)
                charrun_end = m_charrun.end()
                appender(charrun_start, charrun_end, m_charrun.group(1))

            values_end = len(values)
            if charrun_start != values_end:
                values_chunk = values[charrun_end:]
                appender(charrun_end, values_end, values_chunk)

        Insert_prob(many=rows, connection=connection)
        return


def main(args=sys.argv[1:]):
    pass


if __name__ == '__main__':
    sys.exit(main())