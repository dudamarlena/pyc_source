# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/model/Config.py
# Compiled at: 2019-09-26 11:32:58
# Size of source mod 2**32: 705 bytes
import model.ConfigItem as ConfigItem

class Config:
    __doc__ = ' Representing a Config Dict with name\n    author: Julian Gebker\n    version: 1.0.0\n    '

    def __init__(self, name: str, config_nr: int=None, items: list=None):
        """ Constructor
        :param name: Config name
        :param config_nr: Config number
        :param items: Config items
        """
        if items is None:
            self.items = []
        else:
            self.items = items
        self.name = name
        self.config_nr = config_nr

    def add_item(self, item: ConfigItem):
        """ Function adds given item to self.items
        :param item: Item to add
        """
        self.items.append(item)