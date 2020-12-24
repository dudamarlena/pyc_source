# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/solutions/forams/thermometer.py
# Compiled at: 2015-12-21 16:57:02


class Thermometer(object):

    def __init__(self, initial_temperature=0):
        super(Thermometer, self).__init__()
        self.temperature = initial_temperature

    def get_temperature(self):
        return self.temperature