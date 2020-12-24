# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/system/testAmqpProcess.py
# Compiled at: 2011-03-01 14:14:32
"""
Tests in this module require an AMQP exchange to be running,
and need another client sending some data.

Example client::
     nl_write -n 10000 event=stage.end size=13 color=blue foo=baz |      nl_parse bp -a localhost -A exchange=myex -A exchange_type=topic -A route=@event
"""
import sys
from netlogger.amqp.amqp_process import TableBuilder, get_R, bson_decode
from netlogger.tests import shared

class TestCase(shared.BaseTestCase):

    def setUp(self):
        try:
            self._r = get_R()
        except ValueError, err:
            print ('Error getting R instance: {msg}').format(msg=msg)
            raise

    def testTableBuilder(self):
        """Basic usage of TableBuilder class.
        """
        tb = TableBuilder(to_dict=bson_decode, required_attr=['ts', 'event'], last={'event': 'op.end'}, optional_attr=['size', 'speed'], exchange='myexch', exchange_type='topic')
        tb.set_attr_types(auto=True)
        (total, processed, ignored) = (0, 0, 0)
        for (body, was_processed) in tb:
            if was_processed:
                processed += 1
                if (processed + 1) % 100 == 0:
                    df = tb.as_dataframe()
                    if df is not None:
                        print 'Call R analysis function with data frame'
                    else:
                        ignored += 1
                total += 1
                if total > 1000:
                    break

        print ('{n:d} messages: {p:d} processed, {i:d} ignored').format(n=total, p=processed, i=ignored)
        return


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()