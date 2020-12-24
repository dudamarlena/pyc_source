# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\wl\models\general.py
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
__date__ = b'20118-02-03'
from flotils import PrintableBase, FromToDictBase

class Request(FromToDictBase, PrintableBase):

    def __init__(self):
        super(Request, self).__init__()
        self.params = {}

    def to_get_params(self):
        """
        Convert Paramters to HTTP GET parameter dictionary

        :return: GET parameters as dict
        :rtype: dict
        """
        res = {}
        res.update(self.params)
        return res


class Response(FromToDictBase, PrintableBase):

    def __init__(self):
        super(Response, self).__init__()
        self.id = None
        self.stops = None
        self.departures = None
        return


class Location(FromToDictBase, PrintableBase):

    def __init__(self, latitude=None, longitude=None):
        super(Location, self).__init__()
        self.latitude = latitude
        self.longitude = longitude


class Stop(PrintableBase, FromToDictBase):

    def __init__(self):
        super(Stop, self).__init__()
        self.id = None
        self.name = None
        self.distance = None
        self.distance_time = None
        self.location = None
        return

    @classmethod
    def from_dict(cls, d):
        new = super(Stop, Stop).from_dict(d)
        if new.location:
            new.location = Location.from_dict(new.location)
        return new


class Line(PrintableBase, FromToDictBase):

    def __init__(self):
        super(Line, self).__init__()
        self.id = None
        self.name = None
        self.direction = None
        self.realtime = None
        return


class Departure(PrintableBase, FromToDictBase):

    def __init__(self):
        self.stop_id = None
        self.stop_name = None
        self.line_name = None
        self.datetime = None
        self.countdown = None
        self.direction = None
        return