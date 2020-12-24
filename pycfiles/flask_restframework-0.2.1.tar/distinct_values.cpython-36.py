# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/logviewer/flask_validator/resource_mixins/distinct_values.py
# Compiled at: 2017-01-15 10:33:50
# Size of source mod 2**32: 596 bytes
from flask import jsonify
from mongoengine.queryset.queryset import QuerySet
from flask.ext.validator.decorators import list_route

class DistinctValuesMixin:
    distinct_fields = None

    @list_route(methods=['GET'])
    def distinct(self, request):
        assert self.distinct_fields, 'You should set list of allowed fields'
        qs = self.get_queryset()
        field = request.args.get('field')
        if field not in self.distinct_fields:
            return (jsonify([]), 400)
        else:
            assert isinstance(qs, QuerySet)
            return jsonify([item for item in qs.distinct(field)])