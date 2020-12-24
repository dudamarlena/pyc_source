# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/OnePasswordServerItem.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 5217 bytes
import onepassword_tools.lib.OnePasswordItem as OnePasswordItem

class OnePasswordServerItem(OnePasswordItem):
    hostname = None
    hostname: str
    item_type = 'Server'
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
        if item == 'url':
            return self._get_url()
        return super().__getitem__(item)

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                self.__setattr__(key, value)

    def _get_url(self):
        if self.username:
            if self.hostname:
                return 'ssh://%s@%s' % (self.username, self.hostname)
        if self.hostname:
            return 'ssh://%s' % self.hostname
        return

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
            {'inputTraits':{'keyboard': 'URL'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('url'), 
             't':'URL'},
            {'inputTraits':{'autocapitalization':'none', 
              'autocorrection':'no'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('username'), 
             't':'username'},
            {'k':'concealed', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('password'), 
             't':'password'}]},
          {'title':'Admin Console', 
           'name':'Section_%s' % self.opu.generate_op_section_uuid(), 
           'fields':[
            {'inputTraits':{'keyboard': 'URL'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'admin console URL'},
            {'inputTraits':{'autocapitalization':'none', 
              'autocorrection':'no'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'admin console username'},
            {'k':'concealed', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'console password'}]},
          {'title':'Hosting Provider', 
           'name':'Section_%s' % self.opu.generate_op_section_uuid(), 
           'fields':[
            {'inputTraits':{'autocapitalization': 'Words'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'name'},
            {'inputTraits':{'keyboard': 'URL'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'website'},
            {'inputTraits':{'keyboard': 'URL'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'support URL'},
            {'inputTraits':{'keyboard': 'NamePhonePad'}, 
             'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             't':'support phone'}]}]}