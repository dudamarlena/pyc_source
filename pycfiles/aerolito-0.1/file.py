# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/file.py
# Compiled at: 2016-01-14 18:37:25
from .common import ContentState
from .interface import APIObject
from .interface import enable_etags
from .interface import readonly
from .interface import synced

@readonly('id', sync=False)
@synced('name')
@synced('parent')
@readonly('last_modified')
@readonly('size')
@readonly('mime_type')
@readonly('path')
@synced('content')
@readonly('content_state')
class File(APIObject):

    def __init__(self, api, fid=None):
        super(File, self).__init__(api)
        self._id = fid
        self._name = None
        self._parent = None
        self._last_modified = None
        self._size = None
        self._mime_type = None
        self._path = None
        self._content = None
        self._content_state = None
        return

    def from_json(self, json):
        self._id = json['id']
        self._name = json['name']
        if 'parent' in json:
            from .folder import Folder
            self._parent = Folder(self.api, json['parent'])
        self._last_modified = json.get('last_modified')
        self._size = json.get('size')
        self._mime_type = json['mime_type']
        self._content_state = ContentState[json.get('content_state', 'UNKNOWN')]
        return self

    @enable_etags
    def load(self):
        data = self.api.get_file(self.id)
        self.from_json(data)

    @enable_etags
    def load_content(self):
        self._content = self.api.get_file_content(self.id)
        self._mime_type = self.api.response_headers['Content-Type']

    def load_path(self):
        data = self.api.get_folder_path(self.id)
        from .folder import Folder
        self._path = [ Folder(self.api).from_json(f) for f in data['folders'] ]

    def save_content(self, matching=False):
        if not matching:
            self._etags = None
        self.api.upload_file_content(self.id, self._content, ifmatch=self._etags)
        self.load()
        return

    def save_name(self):
        self.move(self.parent.id, self.name, matching=True)

    def save_parent(self):
        self.move(self.parent.id, self.name, matching=True)

    @enable_etags
    def create(self, parent_id, name):
        data = self.api.create_file(parent_id, name)
        self.from_json(data)

    @enable_etags
    def move(self, parent_id, name, matching=False):
        if not matching:
            self._etags = None
        data = self.api.move_file(self.id, parent_id, name, ifmatch=self._etags)
        self.from_json(data)
        return

    def delete(self, matching=False):
        if not matching:
            self._etags = None
        self.api.delete_file(self.id, ifmatch=self._etags)
        return