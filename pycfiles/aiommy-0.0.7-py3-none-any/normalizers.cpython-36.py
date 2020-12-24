# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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