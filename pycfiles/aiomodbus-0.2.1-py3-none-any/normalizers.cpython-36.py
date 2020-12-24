# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/normalizers.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 595 bytes
from playhouse import shortcuts

class CoreNormalizer(object):
    fields = None

    def _model_to_dict(self, model_object):
        raise NotImplemented

    def normalize(self, queryset):
        return [self.normalize_object(i) for i in queryset]

    def normalize_object(self, model_object):
        if self.fields:
            return {field:getattr(model_object, field) for field in self.fields}
        else:
            return shortcuts.model_to_dict(model_object)


class BaseNormalizer(CoreNormalizer):

    def _model_to_dict(self, model_object):
        return shortcuts.model_to_dict(model_object)