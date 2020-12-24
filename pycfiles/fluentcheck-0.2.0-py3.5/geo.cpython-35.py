# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/assertions_is/geo.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 520 bytes
from fluentcheck.assertions_is.base_is import IsBase

class __IsGeo(IsBase):

    @property
    def latitude(self) -> 'Is':
        self.check.is_latitude()
        return self

    @property
    def longitude(self) -> 'Is':
        self.check.is_longitude()
        return self

    @property
    def azimuth(self) -> 'Is':
        self.check.is_azimuth()
        return self

    @property
    def geopoint(self) -> 'Is':
        self.check.is_geopoint()
        return self