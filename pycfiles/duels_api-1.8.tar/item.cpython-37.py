# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Sources\Python\DUELS GAME\duels_api\objects\item.py
# Compiled at: 2019-03-04 16:51:47
# Size of source mod 2**32: 1565 bytes
import logging, duels_api
from duels_api.settings import make_request

class Item:

    def __init__(self, id: str, owner_id: str, type: str, rarity: str, info: str, value: int, log=None):
        self.id = id
        self.owner_id = owner_id
        self.type = type
        self.rarity = rarity
        self.hp = 0
        self.attack = 0
        if log is None:
            self.log = logging.getLogger('Item')
        else:
            self.log = log
        if info == 'Attack':
            self.attack = value
        else:
            if info == 'Health':
                self.hp = value

    def dissasemble(self) -> bool:
        data = '{"partId":"' + str(self.id) + '","id":"' + str(self.owner_id) + '"}'
        j = make_request('inventory/disassemble', data)
        if j:
            self.log.debug('{} Dissasemble item'.format(self.id))
            return True
        self.log.debug('{} Can`t dissasemble'.format(self.id))
        return False

    def equip(self) -> bool:
        data = '{"partId":"' + str(self.id) + '","id":"' + str(self.owner_id) + '"}'
        j = make_request('inventory/equip', data)
        if j:
            self.log.debug('{} Equiped item'.format(self.id))
            return True
        self.log.debug('{} Can`t equip'.format(self.id))
        return False

    def __str__(self):
        return 'Item ID: {} Owner: {} Rarity: {} Attack: {} HP: {}'.format(self.id, self.owner_id, self.rarity, self.attack, self.hp)