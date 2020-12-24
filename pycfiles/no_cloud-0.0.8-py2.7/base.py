# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/no_cloud/remote/base.py
# Compiled at: 2017-01-01 16:24:31


class BaseRemoteStorage(object):

    def __init__(self, config, root):
        self.config = config
        self.root = root

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, *args):
        pass

    def push(self, filename):
        raise NotImplementedError

    def pull(self, path):
        raise NotImplementedError