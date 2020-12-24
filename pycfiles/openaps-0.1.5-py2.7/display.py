# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/glucose/display.py
# Compiled at: 2015-12-15 13:09:24


class Display(object):
    """
        Round Glucose values for display, so that they are consistent in
        all OpenAPS apps

        Example:

            from openaps.glucose.display import Display
            print(Display.display('mmol/L', 5.5))
            print(Display.display('mg/dL', 100))
    """

    @classmethod
    def display(klass, unit, val):
        assert unit in ('mmol/L', 'mg/dL')
        if unit == 'mg/dL':
            return int(round(val))
        if unit == 'mmol/L':
            return round(val, 1)