# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/tempdir.py
# Compiled at: 2011-09-28 13:50:09
import shutil, tempfile

class TempDir:

    def __init__(self, parent_dir=None, prefix='', suffix=''):
        self.__path = tempfile.mkdtemp(dir=parent_dir, prefix=prefix, suffix=suffix)

    def get_path(self):
        return self.__path

    def delete(self):
        shutil.rmtree(self.__path)

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.delete()