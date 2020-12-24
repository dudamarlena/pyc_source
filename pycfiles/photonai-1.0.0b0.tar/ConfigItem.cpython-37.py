# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/model/ConfigItem.py
# Compiled at: 2019-09-26 11:32:58
# Size of source mod 2**32: 337 bytes


class ConfigItem:
    __doc__ = ' Representing a Config Dict Item with name and value\n    author: Julian Gebker\n    version: 1.0.0\n    '

    def __init__(self, name: str, value: str):
        """ Constructor
        :param name: Config name
        :param value: Config value
        """
        self.name = name
        self.value = value