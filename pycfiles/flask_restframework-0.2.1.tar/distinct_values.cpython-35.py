# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/resource_mixins/distinct_values.py
# Compiled at: 2017-01-28 05:34:50
# Size of source mod 2**32: 1386 bytes
from flask import jsonify
from mongoengine.queryset.queryset import QuerySet
from flask_restframework.decorators import list_route

class DistinctValuesMixin:
    __doc__ = '\n    Allows to get distinct values for fields in resource.\n    Example usage::\n\n        >>> class SomeResource(DistinctValuesMixin,\n        >>>                    ModelResource):\n        >>>     serializer_class = SomeSerializer\n        >>>     ordering = ["-created"]\n        >>>     distinct_fields = ["name"]\n        >>>\n        >>>     def get_queryset(self):\n        >>>         return SomeModel.objects.all()\n\n    You should specify required resource attribute **distinct_fields** to list of allowed fields.\n    Then you can make requests::\n\n        GET <resource base url>/distinct?field=<fieldname>\n\n    Response will be list of distinct values of field <fieldname> in database.\n    You can filter response with usual backend filters.\n    '
    distinct_fields = None

    @list_route(methods=['GET'])
    def distinct(self, request):
        assert self.distinct_fields, 'You should set list of allowed fields'
        qs = self.get_queryset()
        qs = self.filter_qs(qs)
        field = request.args.get('field')
        if field not in self.distinct_fields:
            return (jsonify([]), 400)
        assert isinstance(qs, QuerySet)
        return jsonify([item for item in qs.distinct(field)])