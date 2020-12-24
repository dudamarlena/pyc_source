# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/models/Item.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 3469 bytes
import onepassword_local_search.models.Cipher as Cipher
from json import dumps as json_dumps
import onepassword_local_search.exceptions.ManagedException as ManagedException

class Item:
    id: str
    uuid: str
    vault_id: str
    encryptedOverview: Cipher
    encryptedDetails: Cipher
    overview: dict
    details: dict

    def __init__(self, row):
        self.id = row['id']
        self.uuid = row['uuid']
        self.vaultId = row['vault_id']
        self.encryptedOverview = Cipher(row['overview'])
        self.encryptedDetails = Cipher(row['details'])

    def _search_recursive_in_sections(self, field):
        for section in self.details.get('sections'):
            if section.get('fields'):
                for f in section['fields']:
                    if f['t'] == field or f['n'] == field:
                        if 'v' in f.keys():
                            return f['v']

    def _search_recursive_in_section(self, section_name, field):
        for section in self.details.get('sections'):
            if section['title'] == section_name:
                for f in section['fields']:
                    if f['t'] == field or f['n'] == field:
                        if 'v' in f.keys():
                            return f['v']

    def get(self, field=None, strict=True, output=True):
        if field is None:
            self.__delattr__('encryptedOverview')
            self.__delattr__('encryptedDetails')
            return self.output(self, output)
            path = field.split(';;')
            out = None
            if field == 'totp':
                out = self.get_totp()
            else:
                if field in ('title', 'url'):
                    out = self.overview.get(field)
                else:
                    if field in ('username', 'password'):
                        if out is None or out == '':
                            out = self.details.get(field)
                            if out is None:
                                out = self._get_details_field(field)
            if not field == 'notesPlain' or out is None or out == '':
                out = self.details.get(field)
            else:
                pass
        elif not hasattr(self, field) or out is None or out == '':
            out = self.__getattribute__(field)
        else:
            if len(path) > 1 and not out is None:
                if out == '':
                    out = self._search_recursive_in_section(path[0], path[1])
            if out is None and self.details.get('sections'):
                out = self._search_recursive_in_sections(field)
        if strict and out is None:
            raise ManagedException('Unable to find field %s of item %s ' % (field, self.uuid))
        else:
            if not strict:
                if out is None:
                    return ''
            return self.output(out)

    def _get_details_field(self, field):
        if self.details.get('fields'):
            for f in self.details.get('fields'):
                if 'name' in f.keys() and f['name'] == field:
                    return f['value']

    def output(self, content, output=True):
        if not output:
            return content
        out_type = type(content).__name__
        if out_type in ('str', 'int'):
            return content
        return json_dumps(content.__dict__)

    def get_totp(self):
        import pyotp
        token = self._search_recursive_in_sections('One-time password')
        if token:
            return pyotp.TOTP(token.replace(' ', '')).now()
        raise ManagedException('Item %s doesn\'t seem to have a field untitled "One-time password"' % self.uuid)