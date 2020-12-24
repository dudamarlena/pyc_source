# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\examples\timeseries_stateful.py
# Compiled at: 2017-03-25 05:03:59
from evgen.core import SessionTemplate, EventGroup, GenericEventTemplate
from evgen.writers import ConsoleWriter
from evgen.formats import CSVEventFormat
from random import uniform

class TemperatureEventTemplate(GenericEventTemplate):

    def __init__(self, *args, **kwargs):
        GenericEventTemplate.__init__(self, *args, **kwargs)
        self.set_attribute('Temp', self.get_temp)

    def get_temp(self):
        temp_state = self.Session.Attributes.get('TempState')
        current_temp = temp_state + 1
        self.Session.set_attribute('TempState', current_temp)
        return current_temp


eg = EventGroup()
event_format = CSVEventFormat(fields=['TimeStamp', 'SessionId', 'Temp'], sep=' ')
eg.add_event(TemperatureEventTemplate(writer=ConsoleWriter(format=event_format)), probability=1, delay=1000)
eg.set_repeat_policy(min=10, max=10)
session = SessionTemplate()
session.add_event_group(eg)
session.set_attribute('TempState', 20)
session.generate()