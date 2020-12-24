# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/tiles/enums.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 470 bytes


class MapLayerEnum:
    __doc__ = '\n    Allowed map layer values for tiles retrieval\n\n    '
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