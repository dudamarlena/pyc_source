# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\examples\custom_sink.py
# Compiled at: 2017-03-25 04:59:07
from __future__ import print_function
from evgen.core import SessionTemplate, GenericEventTemplate
from evgen.writers import GenericWriter
from evgen.formats import CSVEventFormat, JSONEventFormat

class CustomWriter1(GenericWriter):

    def send(self, event):
        print('JSON:', self.Format.format(event))


class CustomWriter2(GenericWriter):

    def send(self, event):
        print('CSV:', self.Format.format(event))


session = SessionTemplate()
csv_format = CSVEventFormat()
json_format = JSONEventFormat()
json_conn = CustomWriter1(format=json_format)
csv_conn = CustomWriter2(format=csv_format)
start_event = GenericEventTemplate('START')
stop_event = GenericEventTemplate('STOP')
session.add_event(start_event, probability=1)
session.add_event(stop_event, probability=1)
session.add_writer(json_conn)
session.add_writer(csv_conn)
session.generate()