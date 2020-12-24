# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/actioncli/stash_factory.py
# Compiled at: 2020-04-17 19:19:42
# Size of source mod 2**32: 1111 bytes
import logging
from zensols.actioncli import ConfigChildrenFactory, DelegateStash, KeyLimitStash, PreemptiveStash, FactoryStash, DictionaryStash, CacheStash, DirectoryStash, ShelveStash
logger = logging.getLogger(__name__)

class StashFactory(ConfigChildrenFactory):
    USE_CACHE_STASH_KEY = 'use_cache_stash'
    INSTANCE_CLASSES = {}

    def __init__(self, config):
        super(StashFactory, self).__init__(config, '{name}_stash')

    def _instance(self, cls, *args, **kwargs):
        use_cache = False
        if self.USE_CACHE_STASH_KEY in kwargs:
            use_cache = kwargs[self.USE_CACHE_STASH_KEY]
            del kwargs[self.USE_CACHE_STASH_KEY]
        stash = (super(StashFactory, self)._instance)(cls, *args, **kwargs)
        if use_cache:
            stash = CacheStash(stash)
        return stash


for cls in (DelegateStash,
 KeyLimitStash,
 PreemptiveStash,
 FactoryStash,
 DictionaryStash,
 CacheStash,
 DirectoryStash,
 ShelveStash):
    StashFactory.register(cls)