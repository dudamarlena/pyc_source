# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/OnePasswordSSHKeyItem.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 4520 bytes
import onepassword_tools.lib.OnePasswordItem as OnePasswordItem

class OnePasswordSSHKeyItem(OnePasswordItem):
    from_user = None
    from_user: str
    from_host = None
    from_host: str
    to_host = None
    to_host: str
    to_host_abbreviated = None
    to_host_abbreviated: str
    to_ip = None
    to_ip: str
    to_user = None
    to_user: str
    passphrase = None
    passphrase: str
    public_key = None
    public_key: str
    private_key = None
    private_key: str
    item_type = 'Server'
    item_type: str
    title = None
    title: str
    notes = ''
    notes: str
    tags = [
     'Clef SSH']
    tags: []
    url = None
    url: str
    username: str
    to_port = None
    to_port: str

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
        if self.to_host:
            if self.to_user:
                return 'ssh://%s@%s' % (self.to_user, self.to_host)
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
            {'k':'concealed', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('passphrase'), 
             't':'Passphrase'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('to_host'), 
             't':'Hostname'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('to_ip'), 
             't':'IP'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('public_key'), 
             't':'Public Key'},
            {'k':'string', 
             'a':{'multiline': 'yes'}, 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('private_key'), 
             't':'Private Key'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('url'), 
             't':'url'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':str(self.get('to_port')), 
             't':'Port'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('to_host_abbreviated'), 
             't':'Hostname abbreviated'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('to_user'), 
             't':'Remote user'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('from_user'), 
             't':'Local user'},
            {'k':'string', 
             'n':self.opu.generate_op_field_uuid(), 
             'v':self.get('from_host'), 
             't':'Local host'}]}]}