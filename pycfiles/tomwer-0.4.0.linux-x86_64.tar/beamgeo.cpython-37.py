# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/reconstruction/ftseries/params/beamgeo.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 4220 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '07/03/2019'
import enum
from .base import _ReconsParam

@enum.unique
class BeamGeoType(enum.Enum):
    parallel = (0, )
    fan = (2, )
    conical = (3, )


class BeamGeoRP(_ReconsParam):
    __doc__ = 'Beam geometry reconstruction parameters'

    def __init__(self):
        _ReconsParam.__init__(self)
        self._BeamGeoRP__type = BeamGeoType.parallel
        self._BeamGeoRP__sx = 0.0
        self._BeamGeoRP__sy = 0.0
        self._BeamGeoRP__dist = 55.0
        self._managed_params = {'TYPE':self.__class__.type, 
         'SX':self.__class__.sx, 
         'SY':self.__class__.sy, 
         'DIST':self.__class__.dist}

    @property
    def type(self):
        """Beam geometry type"""
        return self._BeamGeoRP__type

    @type.setter
    def type(self, _type):
        if not isinstance(_type, (BeamGeoType, int, str)):
            raise AssertionError
        elif type(_type) is str:
            _BeamGeoRP__type = self._get_beam_geo_frm_letter(_type)
        else:
            _BeamGeoRP__type = BeamGeoType(_type)
        if _BeamGeoRP__type != self._BeamGeoRP__type:
            self._BeamGeoRP__type = _BeamGeoRP__type
            self.changed()

    @property
    def sx(self):
        """Source position on vertical axis(X)"""
        return self._BeamGeoRP__sx

    @sx.setter
    def sx(self, value):
        assert isinstance(value, float)
        if self._BeamGeoRP__sx != value:
            self._BeamGeoRP__sx = value
            self.changed()

    @property
    def sy(self):
        """Source position on vertical axis(Y)"""
        return self._BeamGeoRP__sy

    @sy.setter
    def sy(self, value):
        assert isinstance(value, float)
        if value != self._BeamGeoRP__sy:
            self._BeamGeoRP__sy = value
            self.changed()

    @property
    def dist(self):
        """Source distance in meters"""
        return self._BeamGeoRP__dist

    @dist.setter
    def dist(self, dist):
        assert isinstance(dist, float)
        if self._BeamGeoRP__dist != dist:
            self._BeamGeoRP__dist = dist
            self.changed()

    def to_dict(self):
        _dict = {'TYPE':self.type.name[0], 
         'SX':self.sx, 
         'SY':self.sy, 
         'DIST':self.dist}
        _dict.update(self.unmanaged_params)
        return _dict

    @staticmethod
    def from_dict(_dict):
        params = BeamGeoRP()
        params.load_from_dict(_dict)
        return params

    def load_from_dict(self, _dict):
        self._load_unmanaged_params(_dict)
        self.type = self._get_beam_geo_frm_letter(_dict['TYPE'])
        self.sx = _dict['SX']
        self.sy = _dict['SY']
        self.dist = _dict['DIST']

    @staticmethod
    def _get_beam_geo_frm_letter(letter):
        if letter.lower() == 'p':
            return BeamGeoType.parallel
        if letter.lower() == 'f':
            return BeamGeoType.fan
        if letter.lower() == 'c':
            return BeamGeoType.conical
        raise ValueError('Invalid beam geometry type (%s)' % letter)