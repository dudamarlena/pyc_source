# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/thermometer.py
# Compiled at: 2014-05-15 16:58:29


class Thermometer(object):

    def __init__(self, initial_temperature=0):
        super(Thermometer, self).__init__()
        self.temperature = initial_temperature

    def get_temperature(self):
        return self.temperature