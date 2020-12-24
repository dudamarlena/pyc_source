# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/classes/sensor.py
# Compiled at: 2019-01-10 12:44:21
# Size of source mod 2**32: 1607 bytes
import spiceypy as cspice

class Sensor(object):

    def __init__(self, sensor, host=object(), target=object(), time=object()):
        if isinstance(sensor, str):
            name = sensor
            id = cspice.bodn2c(sensor)
        else:
            id = sensor
            name = cspice.bodc2n(sensor)
        room = 99
        shapelen = 1000
        framelen = 1000
        fov_shape, frame, bsight, n, fov_bounds = cspice.getfov(id, room, shapelen, framelen)
        self.host = host
        self.target = target
        self.time = time
        self.name = name
        self.id = id
        self.fov_shape = fov_shape
        self.frame = frame
        self.bsight_ins = bsight
        self.fov_bounds = fov_bounds
        self.bsight_obs = []
        self.spoint = []

    def getSpoint(self):
        self.bight_obs = []
        self.spoing = []
        for et in self.time.window:
            mat_ins_obs = cspice.pxform(self.frame, self.host.frame, et)
            bsight_obs = cspice.mxv(mat_ins_obs, self.bsight_ins)
            spoint, trgepc, srfvec = cspice.sincpt('Ellipsoid', self.target.name, et, self.target.frame, 'NONE', self.host.name, self.host.frame, bsight_obs)
            self.bsight_obs.append(bsight_obs)
            self.spoint.append(spoint)

        return self.spoint