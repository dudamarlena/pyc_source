# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/OnePasswordItem.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 1779 bytes
import onepassword_tools.lib.OnePasswordUtils as OnePasswordUtils
from onepassword_tools.lib.MiscUtils import remove_null_value_keys_in_dict
import uuid
from abc import ABCMeta, abstractmethod

class OnePasswordItem:
    __metaclass__ = ABCMeta
    createCustomUUID = True
    createCustomUUID: bool

    @property
    @abstractmethod
    def item_type(self) -> str:
        pass

    def __init__(self):
        self.opu = OnePasswordUtils()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        return

    @abstractmethod
    def _request_object(self):
        """
        Static dictionnary reprensenting the request sent to 1Password to create entry
        :return: dict
        """
        pass

    def get(self, item):
        if item is 'notes':
            if getattr(self, item) is None:
                return ''
        return self[item]

    def get_uuid_section(self):
        return {'title':'', 
         'name':'Section_%s' % self.opu.generate_op_section_uuid(), 
         'fields':[
          {'t':'UUID', 
           'v':str(uuid.uuid4()), 
           'k':'string', 
           'n':self.opu.generate_op_field_uuid()}]}

    def get_request_object(self):
        request = self._request_object()
        if self.createCustomUUID:
            request['sections'].append(self.get_uuid_section())
        request = remove_null_value_keys_in_dict(request)
        if 'notesPlain' not in request.keys():
            request['notesPlain'] = ''
        return request