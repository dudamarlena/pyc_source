# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pygoogleearth\camerainfo.py
# Compiled at: 2009-09-26 22:10:50


class CameraInfo(object):

    def __init__(self, comobject):
        self.ge_ci = comobject

    def __getattr__(self, name):
        if name == 'focus_point_latitude':
            return self.ge_ci.FocusPointLatitude
        if name == 'focus_point_longitude':
            return self.ge_ci.FocusPointLongitude
        if name == 'focus_point_altitude':
            return self.ge_ci.FocusPointAltitude
        if name == 'focus_point_altitude_mode':
            return self.ge_ci.FocusPointAltitudeMode
        if name == 'range':
            return self.ge_ci.Range
        if name == 'tilt':
            return self.ge_ci.Tilt
        if name == 'azimuth':
            return self.ge_ci.Azimuth
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'focus_point_latitude':
            self.ge_ci.FocusPointLatitude = value
        elif name == 'focus_point_longitude':
            self.ge_ci.FocusPointLongitude = value
        elif name == 'focus_point_altitude':
            self.ge_ci.FocusPointAltitude = value
        elif name == 'focus_point_altitude_mode':
            self.ge_ci.FocusPointAltitudeMode = value
        elif name == 'range':
            self.ge_ci.Range = value
        elif name == 'tilt':
            self.ge_ci.Tilt = value
        elif name == 'azimuth':
            self.ge_ci.Azimuth = value
        else:
            raise AttributeError