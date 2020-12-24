# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\wl\models\db.py
# Compiled at: 2018-02-03 07:50:03
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2017-18, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.0'
__date__ = b'2018-02-03'
from flotils.convenience import FromToDictBase, format_vars

class Stop(FromToDictBase):

    def __init__(self):
        super(Stop, self).__init__()
        self.id = None
        self.type = None
        self.stop_id = None
        self.name = None
        self.municipality = None
        self.municipality_id = None
        self.lat = None
        self.lng = None
        self.change_date = None
        self.platforms = None
        return

    @classmethod
    def from_csv_row(cls, entry_id, type, diva, name, municipality, municipality_id, lat, lng, change_date):
        return cls.from_dict({b'id': entry_id, 
           b'type': type, 
           b'stop_id': diva, 
           b'name': name, 
           b'municipality': municipality, 
           b'municipality_id': municipality_id, 
           b'lat': lat, 
           b'lng': lng, 
           b'change_date': change_date if change_date else None})

    def __str__(self):
        return (b'<Stop>({})').format(format_vars(self))

    def __repr__(self):
        return self.__str__()


class Line(FromToDictBase):

    def __init__(self):
        super(Line, self).__init__()
        self.id = None
        self.designation = None
        self.order = None
        self.realtime = None
        self.car_type = None
        self.change_date = None
        return

    @classmethod
    def from_csv_row(cls, entry_id, designation, order, realtime, car_type, change_date):
        return cls.from_dict({b'id': entry_id, 
           b'designation': designation, 
           b'order': order, 
           b'realtime': realtime == 1, 
           b'car_type': car_type, 
           b'change_date': change_date if change_date else None})

    def __str__(self):
        return (b'<Line>({})').format(format_vars(self))

    def __repr__(self):
        return self.__str__()


class Platform(FromToDictBase):

    def __init__(self):
        super(Platform, self).__init__()
        self.id = None
        self.line_id = None
        self.stop_id = None
        self.direction = None
        self.order = None
        self.rbl = None
        self.area = None
        self.platform = None
        self.lat = None
        self.lng = None
        self.change_date = None
        self.line = None
        self.stop = None
        return

    @classmethod
    def from_csv_row(cls, entry_id, line_id, stop_id, direction, order, rbl, area, platform, lat, lng, change_date):
        return cls.from_dict({b'id': entry_id, 
           b'line_id': line_id, 
           b'stop_id': stop_id, 
           b'direction': direction, 
           b'order': order, 
           b'rbl': rbl, 
           b'area': area, 
           b'platform': platform, 
           b'lat': lat, 
           b'lng': lng, 
           b'change_date': change_date if change_date else None})

    def __str__(self):
        return (b'<Platform>({})').format(format_vars(self))

    def __repr__(self):
        return self.__str__()