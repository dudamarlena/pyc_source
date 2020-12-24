# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/folder.py
# Compiled at: 2016-01-18 14:27:36
from .interface import APIObject
from .interface import enable_etags
from .interface import readonly
from .interface import synced

@readonly('id', sync=False)
@readonly('files', sync=False)
@readonly('folders', sync=False)
class Children(APIObject):

    def __init__(self, api, pid):
        super(Children, self).__init__(api)
        self._id = pid
        self._files = None
        self._folders = None
        return

    load = lambda x: None

    def from_json(self, json):
        from .file import File
        self._files = frozenset([ File(self.api).from_json(f) for f in json['files']
                                ])
        self._folders = frozenset([ Folder(self.api).from_json(f) for f in json['folders']
                                  ])
        return self


@readonly('id', sync=False)
@synced('name')
@synced('parent')
@readonly('is_shared')
@readonly('shared_folder')
@readonly('path')
@readonly('children')
class Folder(APIObject):

    def __init__(self, api, fid=None):
        super(Folder, self).__init__(api)
        self._id = fid
        self._name = None
        self._parent = None
        self._is_shared = None
        self._shared_folder = None
        self._path = None
        self._children = None
        return

    def from_json(self, json):
        self._id = json['id']
        self._name = json['name']
        if 'parent' in json:
            self._parent = Folder(self.api, json['parent'])
        self._is_shared = json['is_shared']
        if self._is_shared:
            from .shared_folder import SharedFolder
            self._shared_folder = SharedFolder(self.api, json['sid'])
        return self

    @enable_etags
    def load(self):
        data = self.api.get_folder(self.id)
        self.from_json(data)

    def load_children(self):
        data = self.api.get_folder_children(self.id)
        self._children = Children(self.api, self.id).from_json(data)

    def load_path(self):
        data = self.api.get_folder_path(self.id)
        self._path = tuple([ Folder(self.api).from_json(f) for f in data['folders']
                           ])

    def save_name(self):
        self.move(self.parent.id, self.name, matching=True)

    def save_parent(self):
        self.move(self.parent.id, self.name, matching=True)

    @enable_etags
    def create(self, parent_id, name):
        data = self.api.create_folder(parent_id, name)
        self.from_json(data)

    @enable_etags
    def move(self, parent_id, name, matching=False):
        if not matching:
            self._etags = None
        data = self.api.move_folder(self.id, parent_id, name, ifmatch=self._etags)
        self.from_json(data)
        return

    def delete(self, matching=False):
        if not matching:
            self._etags = None
        self.api.delete_folder(self.id, ifmatch=self._etags)
        return