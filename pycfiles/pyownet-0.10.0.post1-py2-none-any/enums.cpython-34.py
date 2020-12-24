# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/tiles/enums.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 470 bytes


class MapLayerEnum:
    """MapLayerEnum"""
    PRECIPITATION = 'precipitation_new'
    WIND = 'wind_new'
    TEMPERATURE = 'temp_new'
    PRESSURE = 'pressure_new'

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of tuples

        """
        return [
         cls.PRECIPITATION,
         cls.WIND,
         cls.TEMPERATURE,
         cls.PRESSURE]