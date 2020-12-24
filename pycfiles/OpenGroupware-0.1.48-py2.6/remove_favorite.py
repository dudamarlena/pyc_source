# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/remove_favorite.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.logic.address import GetCompany
from command import ContactCommand

class RemoveFavorite(Command, ContactCommand):
    __domain__ = 'contact'
    __operation__ = 'remove-favorite'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        self.object_id = int(params.get('id'))

    def run(self):
        favorite_ids = self.get_favorite_ids()
        self.log.debug(favorite_ids)
        if self.object_id in favorite_ids:
            favorite_ids.remove(self.object_id)
            self.set_favorite_ids(favorite_ids)
            self.log.debug(('objectId#{0} remvoed from favorite contacts of objectId#{1}').format(self.object_id, self._ctx.account_id))
        else:
            self.log.debug(('objectId#{0} was not a favorite contact of objectId#{1}').format(self.object_id, self._ctx.account_id))