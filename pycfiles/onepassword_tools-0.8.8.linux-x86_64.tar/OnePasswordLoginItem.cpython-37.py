# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/OnePasswordLoginItem.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 1214 bytes
import onepassword_tools.lib.OnePasswordItem as OnePasswordItem

class OnePasswordLoginItem(OnePasswordItem):
    item_type = 'Login'
    item_type: str
    notes = None
    notes: str
    password = None
    password: str
    tags = [
     'Compte utilisateur']
    tags: []
    url = None
    url: str
    username = None
    username: str

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                self.__setattr__(key, value)

    def _request_object(self):
        """
        Return the dict object with the request sent to 1Password
        :return: dict
        """
        return {'notesPlain':self.get('notes'), 
         'sections':[],  'fields':[
          {'value':self.username, 
           'name':'username', 
           'type':'T', 
           'designation':'username'},
          {'value':self.password, 
           'name':'password', 
           'type':'P', 
           'designation':'password'}]}