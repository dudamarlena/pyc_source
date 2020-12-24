# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\examples\timeseries.py
# Compiled at: 2017-03-24 10:41:42
from evgen.core import SessionTemplate, EventGroup, GenericEventTemplate
from evgen.writers import ConsoleWriter
from random import uniform

class TemperatureEventTemplate(GenericEventTemplate):

    def __init__(self, *args, **kwargs):
        GenericEventTemplate.__init__(self, *args, **kwargs)
        self.set_attribute('Temp', self.get_temp)

    def get_temp(self):
        return round(uniform(18, 34), 4)


eg = EventGroup()
eg.add_event(TemperatureEventTemplate(writer=ConsoleWriter()), probability=1, delay=1000, delay_random=0.5)
eg.set_repeat_policy(min=10, max=10)
session = SessionTemplate()
session.add_event_group(eg)
session.generate()