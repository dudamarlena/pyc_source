# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/amqp/amqp_process.py
# Compiled at: 2011-03-01 14:15:04
"""
Process AMQP messages

Example usage::
      import sys
      from netlogger.amqp.amqp_process import TableBuilder, get_R, bson_decode

      try:
          r = get_R()
      except ValueError, err:
          print('Error getting R instance: {msg}'.format(msg=msg))
          sys.exit(1)
      tb = TableBuilder(to_dict=bson_decode, required_attr=['ts', 'event'],
                        last={'event':'op.end'}, optional_attr=['size', 'speed'],
                        exchange='myexch', type='topic')
      tb.set_attr_types(auto=True) # infer types from 1st row of data
      total, processed, ignored = 0, 0, 0
      for (body, was_processed) in tb:
           if was_processed:
               processed += 1
               if (processed + 1) % 100 == 0:
                   df = tb.as_dataframe()
                   if df is not None:
                       r.my_analysis_function(df)
           else:
               ignored += 1
           total += 1
      print('{n:d} messages: {p:d} processed, {i:d} ignored'.format(n=total, p=processed,
            i=ignored))
               
"""
import csv, logging, sys, time, warnings
from amqplib import client_0_8 as amqp
bson_decode = None
try:
    import bson
    if hasattr(bson, 'dumps'):
        bson_decode = bson.loads
    else:
        bson_decode = bson.BSON().decode
except ImportError, err:
    warnings.warn(('Cannot import bson: {0}').format(err))

from netlogger.nllog import get_logger, DoesLogging
try:
    from netlogger.analysis.datamining import rpython
except ImportError, err:
    warnings.warn(('Cannot import rpy2: {0}').format(err))
    rpython = None

def get_R():
    """Get shared R instance."""
    if rpython is None:
        raise ValueError('R library not imported')
    return rpython.R


class Reader:
    """Read from AMQP
    """

    def __init__(self, host='localhost', port=5672, exchange=None, exchange_type='direct', routing_key='#', queue='testq', auto_delete=True, durable=False, no_ack=True):
        conn = amqp.Connection(host=host, port=port)
        chan = conn.channel()
        chan.exchange_declare(exchange, type=exchange_type, durable=durable, auto_delete=auto_delete)
        chan.queue_declare(queue)
        chan.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)
        tag = chan.basic_consume(queue=queue, callback=self.process, no_ack=no_ack)
        self._conn, self._chan, self._tag = conn, chan, tag

    def __iter__(self):
        return self

    def process(self, msg):
        self._item = msg.body

    def next(self):
        self._chan.wait()
        return self._item


class Table:
    """Fill a table of values.
    """

    def __init__(self, attrs, last=None):
        """Create a table whose columns are the list given in 'attrs'.
        
        If 'last' is non-empty, then it should be dictionary. In this case,
        methods to return (and clear) data will operate on boundaries
        where all attributes in the dictionary match the contents of the row.
        For example, last={'event':'something.end'}
        would make sure that 'something.end' was the value in the 'event' column for the
        last row in a given dataframe. Rows after that would be saved to start the
        dataframe in the next chunk returned.
        All keys in 'last' must be present as attributes in 'attrs'.
        """
        if last:
            self._last = []
            for a in last:
                try:
                    idx = attrs.index(a)
                except ValueError:
                    raise ValueError(("attribute {a} in 'last' missing from 'attrs'").format(a=a))

                self._last.append((idx, last[a]))

        else:
            self._last = None
        self._attrs = attrs
        self._rows = []
        self._atypes, self._magictypes = None, False
        return

    def set_attr_types(self, auto=False, attr_types=[]):
        """Set type for each attribute, first required then optional ones,
        given to the constructor. This is only needed for R output.

        Args:
          auto - If True, set flag to auto-determine types from next input row
          attr_types - If auto is false, use this value
        """
        if auto:
            self._magictypes = True
        else:
            assert len(attr_types) == len(self._attrs), 'attr_types length != attrs length'
            self._atypes = attr_types

    def add_row(self, row):
        self._rows.append(row)

    def _find_last(self):
        if self._last is None:
            return len(self._rows) - 1
        else:
            for i in xrange(len(self._rows) - 1, -1, -1):
                row, match = self._rows[i], True
                for (idx, val) in self._last:
                    if row[idx] != val:
                        match = False
                        break

                if match:
                    return i

            return -1

    def _clear(self, last):
        self._rows = self._rows[last + 1:]

    def write_csv(self, writer, clear=True, hdr=False):
        """Write csv to 'writer', which should have a method 'writerow([ ])'.
        If hdr is True, add a row of attr names.
        """
        n = self._find_last()
        if n >= 0:
            if hdr:
                writer.writerow(self._attrs)
            for i in xrange(n + 1):
                writer.writerow(self._rows[i])

            if clear:
                self._clear(n)

    def get_rdata(self, clear=True):
        """Return contents as an R dataframe.
        
        If clear is true, clear contents (e.g. for chunked processing),
        otherwise leave them alone.
        """
        df = None
        n = self._find_last()
        if n >= 0:
            if self._atypes is None:
                if self._magictypes:
                    self._atypes = [ rpython.COLTYPE.from_value(x) for x in self._rows[0] ]
                else:
                    self._atypes = [
                     rpython.COLTYPE.STR] * len(self._attrs)
            df = rpython.make_data_frame(self._rows[:n + 1], self._attrs, self._atypes)
            if clear:
                self._clear(n)
        return df


class TableBuilder(Reader, Table):

    def __init__(self, to_dict=None, required_attr=[], optional_attr=[], next_in_chain=None, last=None, **kw):
        """Build a table.
        
        Each incoming message is parsed with to_dict(),
        then required_attr are extracted; if any is missing the message is invalid.
        Then optional_attr are extracted; missing values ignored.
        If valid, the resulting row is added.
        If the row was invalid and 'next_in_chain' is non-empty, then next_in_chain
          should be a TableBuilder obj, and the parsed data will be
          passed to next_in_chain.process(), which will return true if the message
          was (eventually) valid, or False otherwise.
        See Table for details on the 'last' argument.
        
        """
        self._parse = to_dict
        self._req, self._opt = required_attr, optional_attr
        self._next = next_in_chain
        Reader.__init__(self, **kw)
        Table.__init__(self, required_attr + optional_attr, last=last)

    def process(self, msg):
        """Process a message.

        Return: was-processed
        """
        if hasattr(msg, 'body'):
            data = self._parse(msg.body)
        else:
            data = msg
        row, had_req = [], True
        for a in self._req:
            v = data.get(a, None)
            if v is None:
                had_req = False
                break
            row.append(v)

        if not had_req:
            if self._next:
                self._valid = self._next.process(data)
        else:
            for a in self._opt:
                v = data.get(a, None)
                if v:
                    row.append(v)
                else:
                    row.append('')

            self.add_row(row)
            self._valid = True
        self._item = (
         msg.body, self._valid)
        return self._valid

    def get_next(self):
        return self._next