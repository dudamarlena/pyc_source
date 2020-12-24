# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\obj\origin.py
# Compiled at: 2019-12-07 13:33:32
# Size of source mod 2**32: 2306 bytes
from datetime import datetime

class Origin:
    __doc__ = '\n\n        Describes the origin of a :class:`Connection`.\n\n        Attributes\n        -----------\n\n        raw :class:`dict`\n            Raw dict received by the API.\n        is_global_id :class:`bool`\n            ~\n        id :class:`str`\n            station id of the origin station\n        name :class:`str`\n            name of the origin station\n        disassembled_name Optional[:class:`str`]\n            detailed name of the origin station.\n        type :class:`str`\n            type of the origin station. (e.g. bus, track)\n        point_type Optional[:class:`str`]\n            ~\n        coord List[:class:`int`]\n            coords of the station\n        niveau :class:`int`\n            ~\n        parent :class:`dict`\n            ~\n        departure_time_planned :class:`datetime.datetime`\n            Time planned of arrival.\n        departure_time_estimated :class:`datetime.datetime`\n            Time estimated with realtime info (same as `departure_time_planned` if no realtime data is available).\n        delay :class:`int`\n            Minutes of delay.\n        properties :class:`dict`\n            misc info about the origin.\n    '

    def __init__(self, **kwargs):
        self.is_global_id = kwargs.get('isGlobalId')
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.disassembled_name = (kwargs.get('disassembledName'),)
        self.type = kwargs.get('type')
        self.point_type = kwargs.get('pointType')
        self.coord = tuple(kwargs.get('coord', []))
        self.niveau = kwargs.get('niveau')
        self.parent = kwargs.get('parent')
        self.departure_time_planned = datetime.strptime(kwargs.get('departureTimePlanned', '')[:-1], '%Y-%m-%dT%H:%M:%S')
        self.departure_time_estimated = datetime.strptime(kwargs.get('departureTimeEstimated', '')[:-1], '%Y-%m-%dT%H:%M:%S')
        delta = self.departure_time_estimated - self.departure_time_planned
        self.delay = int(delta.total_seconds() / 60)
        self.raw = kwargs
        self.properties = kwargs.get('properties')