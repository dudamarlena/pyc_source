# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/migrate_tool/services/LocalFileSystem.py
# Compiled at: 2017-03-29 00:21:31
from __future__ import absolute_import, print_function, with_statement
import os
from os import path
from migrate_tool.task import Task
from migrate_tool import storage_service

class LocalFileSystem(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        self._workspace = kwargs['workspace']

    def exists(self, path_):
        rt = path.join(self._workspace, path_)
        return path.exists(rt)

    def download(self, task, localpath):
        path_ = task['key']
        src_path = path.join(self._workspace, path_)
        import shutil
        return shutil.copyfile(src_path, localpath)

    def upload(self, task, localpath):
        path_ = task['key']
        src_path = path.join(self._workspace, path_)
        try:
            import os
            os.makedirs(path.dirname(src_path))
        except OSError:
            pass

        import shutil
        return shutil.copyfile(localpath, src_path)

    def list(self):
        for file in os.listdir(self._workspace):
            from os import path
            yield Task(file, path.getsize(file), None)

        return


def make():
    """ hook function for entrypoints

    :return:
    """
    return LocalFileSystem


if __name__ == '__main__':
    import os
    fs = LocalFileSystem(workspace=os.getcwd())
    for f in fs.list():
        print(f)