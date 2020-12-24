# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\obj\departure.py
# Compiled at: 2019-12-07 13:33:32
# Size of source mod 2**32: 4038 bytes
from datetime import datetime
from .serving_line import ServingLine
from .line_operator import LineOperator

class Departure:
    __doc__ = '\n\n     Departure object from a departure request of one station.\n\n    Attributes\n    -----------\n\n    raw :class:`dict`\n        Raw dict received by the API.\n    stop_id :class:`str`\n        Station_id of the departure.\n    x :class:`str`\n        Coordinates of the station.\n    y :class:`str`\n        Coordinates of the station.\n    map_name :class:`str`\n        Map name the API works on.\n    area :class:`str`\n        The area of the station (unsure atm)\n    platform :class:`str`\n        Platform / track of the departure.\n    platform_name :class:`str`\n        name of the platform.\n    stop_name :class:`str`\n        name of the station.\n    name_wo :class:`str`\n        name of the station.\n    countdown :class:`int`\n        minutes until departure.\n    datetime :class:`datetime.datetime`\n        Planned departure datetime.\n    real_datetime :class:`datetime.datetime`\n        Estimated departure datetime (equal to ``self.datetime`` if no realtime data is available).\n    delay :class:`int`\n        Delay of departure in minutes.\n    serving_line :class:`ServingLine`\n        line of the incoming departure.\n    operator :class:`LineOperator`\n        Operator of the incoming departure.\n    stop_infos: Optional[:class:`dict`]\n        All related info to the station (e.g. maintenance work).\n    line_infos Optional[:class:`dict`]\n        All related info to the station (e.g. maintenance work).\n    '

    def __init__(self, **kwargs):
        self.stop_id = kwargs.get('stopID')
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.map_name = kwargs.get('mapName')
        self.area = kwargs.get('area')
        self.platform = kwargs.get('platform')
        self.platform_name = kwargs.get('platformName')
        self.stop_name = kwargs.get('stopName')
        self.name_wo = kwargs.get('nameWO')
        self.point_type = kwargs.get('pointType')
        self.countdown = int(kwargs.get('countdown', '0'))
        dt = kwargs.get('dateTime')
        if dt:
            try:
                self.datetime = datetime(year=(int(dt.get('year', datetime.now().year))),
                  month=(int(dt.get('month', datetime.now().month))),
                  day=(int(dt.get('day', datetime.now().day))),
                  hour=(int(dt.get('hour', datetime.now().hour))),
                  minute=(int(dt.get('minute', datetime.now().minute))))
            except ValueError:
                pass

        else:
            self.datetime = None
        r_dt = kwargs.get('realDateTime')
        if r_dt:
            try:
                self.real_datetime = datetime(year=(int(r_dt.get('year', datetime.now().year))),
                  month=(int(r_dt.get('month', datetime.now().month))),
                  day=(int(r_dt.get('day', datetime.now().day))),
                  hour=(int(r_dt.get('hour', datetime.now().hour))),
                  minute=(int(r_dt.get('minute', datetime.now().minute))))
            except ValueError:
                pass

        else:
            self.real_datetime = self.datetime
        self.delay = int((self.real_datetime - self.datetime).total_seconds() / 60)
        self.serving_line = ServingLine(**kwargs.get('servingLine', {}))
        self.operator = LineOperator(**kwargs.get('operator', {}))
        self.raw = kwargs
        self.stop_infos = kwargs.get('stopInfos')
        self.line_infos = kwargs.get('lineInfos')

    def __str__(self):
        pre = '[Delayed] ' if self.delay else ''
        if self.real_datetime.date() == datetime.now().date():
            return f"{pre}[{str(self.real_datetime.strftime('%H:%M'))}] {self.serving_line}"
        return f"{pre}[{str(self.real_datetime)}] {self.serving_line}"