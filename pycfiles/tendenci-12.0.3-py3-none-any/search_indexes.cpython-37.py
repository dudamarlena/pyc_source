# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/search_indexes.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 705 bytes
from haystack import indexes
from tendenci.apps.videos.models import Video
from tendenci.apps.perms.indexes import TendenciBaseSearchIndex
from tendenci.apps.base.utils import strip_html

class VideoIndex(TendenciBaseSearchIndex):
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    ordering = indexes.IntegerField(model_attr='ordering')
    category = indexes.CharField()
    order = indexes.DateTimeField()

    @classmethod
    def get_model(self):
        return Video

    def prepare_description(self, obj):
        return strip_html(obj.description)

    def prepare_order(self, obj):
        return obj.create_dt