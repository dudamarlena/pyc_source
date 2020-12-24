# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/record.py
# Compiled at: 2020-01-12 12:29:08
# Size of source mod 2**32: 4924 bytes


class Record(object):

    @property
    def record_capability(self):
        ret = self.command('recordManager.cgi?action=getCaps')
        return ret.content.decode('utf-8')

    @property
    def record_config(self):
        ret = self.command('configManager.cgi?action=getConfig&name=Record')
        return ret.content.decode('utf-8')

    @record_config.setter
    def record_config(self, rec_opt):
        """
        rec_opt is the Record options listed as example below:

        +----------------------+--------+------------------------------------+
        | ParamName            | Value  |   Description                      |
        +----------------------+--------+------------------------------------+
        | Record[ch].PreRecord |Integer | Range is [0-300]                   |
        |                      |        | Prerecord seconds, 0 no prerecord  |
        |                      |        | ch (Channel number) starts from 0  |
        +----------------------|--------|------------------------------------+
        | Record[ch].          |        | wd (week day)                      |
        | TimeSection[wd][ts]  | string | range is [0-6] (Sun/Sat)           |
        |                      |        |                                    |
        |                      |        | ts (time section) range is [0-23]  |
        |                      |        | time section table index           |
        |                      |        |                                    |
        |                      |        | Format: mas hh:mm:ss-hh:mm:ss      |
        |                      |        | Mask: [0-65535], hh: [0-24],       |
        |                      |        | mm: [0-59], ss: [0-59]             |
        |                      |        | Mask indicate record type by bits: |
        |                      |        | Bit0: regular record               |
        |                      |        | Bit1: motion detection record      |
        |                      |        | Bit2: alarm record                 |
        |                      |        | Bit3: card record                  |
        +----------------------+--------+------------------------------------+

        Example:
        Record[0].TimeSection[0][0]=6 00:00:00-23:59:59

        rec_opt format:
        <paramName>=<paramValue>[&<paramName>=<paramValue>...]
        """
        ret = self.command('configManager.cgi?action=setConfig&{0}'.format(rec_opt))
        return ret.content.decode('utf-8')

    @property
    def media_global_config(self):
        ret = self.command('configManager.cgi?action=getConfig&name=MediaGlobal')
        return ret.content.decode('utf-8')

    @property
    def record_mode(self):
        status_code = {0:'Automatic',  1:'Manual', 
         2:'Stop', 
         None:'Unknown'}
        ret = self.command('configManager.cgi?action=getConfig&name=RecordMode')
        try:
            status = int([s for s in ret.content.decode('utf-8').split() if 'Mode=' in s][0].split('=')[(-1)])
        except:
            status = None

        return status_code[status]

    @record_mode.setter
    def record_mode(self, record_opt, channel=0):
        """
        Params:

        channel:
        video index, start from 0

        record_opt:
        +----------------------------+-----------------+-------------------+
        | ParamName                  | ParamValue type | Description       |
        +----------------------------+-----------------+-------------------+
        | RecordMode[channel].Mode   | integer         | Range os {0, 1, 2}|
        |                            |                 | 0: automatically  |
        |                            |                 | 1: manually       |
        |                            |                 | 2: stop record    |
        +----------------------------+-----------------+-------------------+

        record_opt format:
        <paramName>=<paramValue>[&<paramName>=<paramValue>...]
        """
        ret = self.command('configManager.cgi?action=setConfig&RecordMode[{0}].Mode={1}'.format(channel, record_opt))
        return ret.content.decode('utf-8')