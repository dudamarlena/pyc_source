# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/search_indexes.py
# Compiled at: 2016-07-29 08:17:51
# Size of source mod 2**32: 657 bytes
import datetime
from haystack import indexes
from .models import TransTask

class TransTaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    has_value = indexes.CharField(model_attr='has_value')
    language = indexes.CharField(model_attr='language')
    user = indexes.CharField(model_attr='user')

    def get_model(self):
        return TransTask

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.filter(date_creation__lte=datetime.datetime.now())