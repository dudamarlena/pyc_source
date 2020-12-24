# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\obj\serving_line.py
# Compiled at: 2019-12-10 14:27:31
# Size of source mod 2**32: 2405 bytes


class ServingLine:
    __doc__ = '\n\n        Describes the line, departing or arriving in a Departure/Arrival result.\n\n        Attributes\n        -----------\n\n        raw :class:`dict`\n            Raw dict received by the API.\n        key :class:`str`\n            key (most likely an ID) of the line.\n        code :class:`str`\n            code (most likely type) of the line.\n        number :class:`str`\n            number of line (e.g. U12).\n        symbol :class:`str`\n            symbol displayed on the transport itself (e.g. U12).\n        mot_type :class:`str`\n            ~\n        mt_sub_code :class:`str`\n            ~\n        real_time :class:`bool`\n            whether or not the transport supports realtime tracking.\n        direction :class:`str`\n            Last station the transport is heading to.\n        direction :class:`str`\n            Last station the transport is heading to.\n        direction_from :class:`str`\n            Starting station of the transport.\n        name :class:`str`\n            name of the line type (e.g. Stadtbahn).\n        train_num :class:`str`\n            Last station the transport is heading to.\n        delay Optional[:class:`str`]\n            Minutes of delay.\n        li_erg_ri_proj :class:`dict`\n            Detailed line information (e.g. network)\n        dest_id :class:`str`\n            station id of the destination\n        stateless :class:`str`\n            ~\n    '

    def __init__(self, **kwargs):
        self.raw = kwargs
        self.key = kwargs.get('key')
        self.code = kwargs.get('code')
        self.number = kwargs.get('number')
        self.symbol = kwargs.get('symbol')
        self.mot_type = kwargs.get('motType')
        self.mt_sub_code = kwargs.get('mtSubCode')
        try:
            self.real_time = bool(int(kwargs.get('realtime', '0')))
        except ValueError:
            self.real_time = False
        else:
            self.direction = kwargs.get('direction')
            self.direction_from = kwargs.get('directionFrom')
            self.name = kwargs.get('trainName', kwargs.get('name'))
            self.delay = kwargs.get('delay')
            self.li_erg_ri_proj = kwargs.get('liErgRiProj')
            self.dest_id = kwargs.get('destID')
            self.stateless = kwargs.get('stateless')

    def __str__(self):
        return f"[{self.symbol}]: {self.direction_from} - {self.direction}"