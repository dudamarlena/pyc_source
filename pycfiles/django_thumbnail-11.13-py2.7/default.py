# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sorl/thumbnail/default.py
# Compiled at: 2012-12-12 10:05:53
from django.utils.functional import LazyObject
from sorl.thumbnail.conf import settings
from sorl.thumbnail.helpers import get_module_class

class Backend(LazyObject):

    def _setup(self):
        self._wrapped = get_module_class(settings.THUMBNAIL_BACKEND)()


class KVStore(LazyObject):

    def _setup(self):
        self._wrapped = get_module_class(settings.THUMBNAIL_KVSTORE)()


class Engine(LazyObject):

    def _setup(self):
        self._wrapped = get_module_class(settings.THUMBNAIL_ENGINE)()


class Storage(LazyObject):

    def _setup(self):
        self._wrapped = get_module_class(settings.THUMBNAIL_STORAGE)()


backend = Backend()
kvstore = KVStore()
engine = Engine()
storage = Storage()