# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/output/values.py
# Compiled at: 2012-10-06 13:41:05
from mole.output import Output, OutputError
from mole.event import Event

class OutputValues(Output):

    def __init__(self, fields=[]):
        self.fields = fields

    def __call__(self, pipeline):
        for event in pipeline:
            if not isinstance(event, Event):
                raise OutputError('Unable to output without parser. Offending type is %s' % event.__class__)
            yield (' ').join(map(lambda (x, y): '%s="%s"' % (x, y), filter(lambda (x, y): not self.fields or x in self.fields, [ x for x in event ])))