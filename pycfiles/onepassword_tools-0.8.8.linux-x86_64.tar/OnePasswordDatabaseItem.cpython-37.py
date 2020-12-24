# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/OnePasswordDatabaseItem.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 3456 bytes
import onepassword_tools.lib.OnePasswordItem as OnePasswordItem

class OnePasswordDatabaseItem(OnePasswordItem):
    database = None
    database: str
    hostname = None
    hostname: str
    item_type = 'Database'
    item_type: str
    notes = None
    notes: str
    password = None
    password: str
    port = None
    port: str
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
         'sections':[
          {'title':'', 
           'name':'Section_%s' % self.opu.generate_op_section_uuid(), 
           'fields':[
            {'k':'menu', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'type'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.hostname, 
             't':'server'},
            {'inputTraits':{'keyboard': 'NumberPad'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.port, 
             't':'port'},
            {'inputTraits':{'autocapitalization':'none', 
              'autocorrection':'no'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.database, 
             't':'database'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.username, 
             't':'username'},
            {'k':'concealed', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.password, 
             't':'password'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'SID'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'alias'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'connection options'}]}]}