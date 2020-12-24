# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/diogo.munaro/workspace/jupyterhub_hook_filemanager/jupyterhub_hook_filemanager/hook_filemanager.py
# Compiled at: 2017-01-30 12:08:01
# Size of source mod 2**32: 2341 bytes
from notebook.services.contents.filemanager import FileContentsManager
from traitlets import Any

class HookFileContentsManager(FileContentsManager):
    __doc__ = 'Local spawner that runs single-user servers as the same user as the Hub itself.\n\n    Overrides user-specific env setup with no-ops.\n    '
    pre_get_hook = Any(None, config=True, help='Python callable thereof\n        to be called before getting a notebook.\n        ')
    post_get_hook = Any(None, config=True, help='Python callable thereof\n        to be called after getting a notebook.\n        ')
    pre_update_hook = Any(None, config=True, help='Python callable thereof\n        to be called before update a notebook.\n        ')
    post_update_hook = Any(None, config=True, help='Python callable thereof\n        to be called after update a notebook.\n        ')
    pre_delete_hook = Any(None, config=True, help='Python callable thereof\n        to be called before delete a notebook.\n        ')
    post_delete_hook = Any(None, config=True, help='Python callable thereof\n        to be called after delete a notebook.\n        ')

    def get(self, path, content=True, type=None, format=None):
        if self.pre_get_hook:
            self.pre_get_hook(path=path, content=content, type=type, format=format, contents_manager=self)
        returned = super(HookFileContentsManager, self).get(path, content, type, format)
        if self.post_get_hook:
            self.post_get_hook(path=path, content=content, type=type, format=format, contents_manager=self)
        return returned

    def update(self, model, path):
        if self.pre_update_hook:
            self.pre_update_hook(model=model, path=path, contents_manager=self)
        returned = super(HookFileContentsManager, self).update(model, path)
        if self.post_update_hook:
            self.post_update_hook(model=model, path=path, contents_manager=self)
        return returned

    def delete(self, path):
        if self.pre_delete_hook:
            self.pre_delete_hook(path=path, contents_manager=self)
        returned = super(HookFileContentsManager, self).delete(path)
        if self.post_delete_hook:
            self.post_delete_hook(path=path, contents_manager=self)
        return returned