# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/add_favorite.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.logic.address import GetCompany
from command import ContactCommand

class AddFavorite(Command, ContactCommand):
    __domain__ = 'contact'
    __operation__ = 'add-favorite'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        self.object_id = int(params.get('id'))

    def run(self):
        favorite_ids = self.get_favorite_ids()
        if self.object_id not in favorite_ids:
            favorite_ids.append(self.object_id)
            self.set_favorite_ids(favorite_ids)