# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/narani/Projects/django-zen-queries/zen_queries/rest_framework.py
# Compiled at: 2020-03-13 12:34:20
# Size of source mod 2**32: 779 bytes
from zen_queries import queries_disabled

class QueriesDisabledSerializerMixin(object):

    @property
    def data(self):
        with queries_disabled():
            return super(QueriesDisabledSerializerMixin, self).data


def disable_serializer_queries(serializer):
    serializer.__class__ = type(serializer.__class__.__name__, (
     QueriesDisabledSerializerMixin, serializer.__class__), {})
    return serializer


class QueriesDisabledViewMixin(object):

    def get_serializer(self, *args, **kwargs):
        serializer = (super(QueriesDisabledViewMixin, self).get_serializer)(*args, **kwargs)
        if self.request.method == 'GET':
            serializer = disable_serializer_queries(serializer)
        return serializer