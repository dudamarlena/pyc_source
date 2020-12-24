# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\obj\connection.py
# Compiled at: 2020-01-09 14:01:54
# Size of source mod 2**32: 2903 bytes
from datetime import datetime
from .origin import Origin
from .destination import Destination
from .transportation import Transportation

class Connection:
    __doc__ = '\n\n        Several connections describe one :class:`Trip`.\n\n\n        Attributes\n        -----------\n\n        raw :class:`dict`\n            Raw dict received by the API.\n        duration :class:`int`\n            seconds this connection takes\n        is_realtime_controlled :class:`bool`\n            whether or not this connection has realtime tracking\n        origin :class:`Origin`\n            Origin, where this connection starts\n        destination :class:`Destination`\n            Where this connection is heading to\n        transportation :class:`Transportation`\n            Transportation info of this connection\n        stop_sequence Optional[List[:class:`dict`]]\n            stop sequence of this connection\n        foot_path_info Optional[]\n            Info if you really want to walk ?\n        infos Optional[List[]]\n            ~\n        coords Optional[List[List[:class:`int`]]]\n            coords of this connection\n        path_description Optional[]\n            ~\n        interchange Optional[]\n            ~\n        properties Optional[:class:`dict`]\n            misc info about this connection\n    '

    def __init__(self, **kwargs):
        self.duration = kwargs.get('duration')
        self.is_realtime_controlled = kwargs.get('isRealtimeControlled', False)
        self.origin = Origin(**kwargs.get('origin'))
        self.destination = Destination(**kwargs.get('destination'))
        self.transportation = Transportation(**kwargs.get('transportation'))
        self.raw = kwargs
        self.stop_sequence = kwargs.get('stopSequence')
        self.foot_path_info = kwargs.get('footPathInfo')
        self.infos = kwargs.get('infos')
        self.coords = kwargs.get('coords')
        self.path_description = kwargs.get('pathDescription')
        self.interchange = kwargs.get('interchange')
        self.properties = kwargs.get('properties')

    def __str__(self):
        dep_pre = '[Delayed] ' if self.origin.delay else ''
        arr_pre = '[Delayed] ' if self.destination.delay else ''
        if self.origin.departure_time_estimated.date() == datetime.now().date():
            return f"[{self.transportation.disassembled_name}]: {dep_pre}[{self.origin.departure_time_estimated.strftime('%H:%M')}] @ {self.origin.name} - {arr_pre}[{self.destination.arrival_time_estimated.strftime('%H:%M')}] @ {self.destination.name}"
        return f"[{self.transportation.disassembled_name}]: {dep_pre}[{self.origin.departure_time_estimated}] @ {self.origin.name} - {arr_pre}[{self.destination.arrival_time_estimated}] @ {self.destination.name}"