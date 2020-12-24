# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/search/indexes.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 912 bytes
from haystack import indexes
from django.db.models import signals
from tendenci.apps.search.signals import save_unindexed_item

class CustomSearchIndex(indexes.SearchIndex):
    __doc__ = '\n    A custom SearchIndex subclass that saves the objects to the UnindexedItem table\n    (if not already added) for later processing and deletes objects immediately.\n\n    This requires a script to run the management command "process_unindexed" in the\n    background to update index.\n    '

    def _setup_save(self, model):
        signals.post_save.connect(save_unindexed_item, sender=model, weak=False)

    def _teardown_save(self, model):
        signals.post_save.disconnect(save_unindexed_item, sender=model)

    def _setup_delete(self, obj):
        signals.post_delete.connect((self.remove_object), sender=obj)

    def _teardown_delete(self, obj):
        signals.post_delete.disconnect((self.remove_object), sender=obj)