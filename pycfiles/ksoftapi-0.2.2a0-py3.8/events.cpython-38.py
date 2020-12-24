# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ksoftapi\events.py
# Compiled at: 2020-04-19 14:32:46
# Size of source mod 2**32: 278 bytes


class BanUpdateEvent:

    def __init__(self, data: dict):
        self.id = data['id']
        self.moderator_id = data['moderator_id']
        self.reason = data['reason']
        self.proof = data['proof']
        self.active = data['active']