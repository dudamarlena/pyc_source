# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/lib/data_structures/persistent_dictionary.py
# Compiled at: 2017-12-28 15:07:06
import os, os.path
try:
    import cPickle as pickle
except ImportError:
    import pickle

import shutil, threading
from future.utils import with_metaclass
from flawless.lib.data_structures import ProxyContainerMethodsMetaClass

class PersistentDictionary(with_metaclass(ProxyContainerMethodsMetaClass, object)):
    """ Provides a persistent thread-safe dictionary that is backed by a file on disk """

    def _proxyfunc_(self, attr, *args, **kwargs):
        with self.lock:
            return getattr(self.dict, attr)(*args, **kwargs)

    def __init__(self, file_path):
        self.lock = threading.RLock()
        self.file_path = file_path
        self.dict = None
        return

    def open(self):
        with self.lock:
            if os.path.isfile(self.file_path):
                fh = open(self.file_path, 'rb+')
                self.dict = pickle.load(fh)
                fh.close()
            else:
                self.dict = dict()

    def sync(self):
        with self.lock:
            fh = open(self.file_path + '.tmp', 'wb+')
            pickle.dump(self.dict, fh, pickle.HIGHEST_PROTOCOL)
            fh.close()
            shutil.move(self.file_path + '.tmp', self.file_path)

    def close(self):
        pass

    def get_path(self):
        return self.file_path