# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/filter_backends.py
# Compiled at: 2017-11-03 05:35:30
# Size of source mod 2**32: 2460 bytes
import json

class BaseBackend:

    def __init__(self, qs, request, resource):
        self.qs = qs
        self.request = request
        self.resource = resource

    def filter(self):
        raise NotImplementedError


class OrderingBackend(BaseBackend):
    __doc__ = '\n    Allows ordering with GET parameter.\n    For example,\n\n        GET ?ordering=name,-value\n\n    Will sort .order_by(["name", "-value"])\n\n    You can set resource attribute **ordering** if you want default ordering\n    '

    def _default_ordering(self):
        if hasattr(self.resource, 'ordering'):
            return self.resource.ordering
        return []

    def filter(self):
        try:
            ordering_fields = self.request.args.get('ordering')
            if ordering_fields:
                ordering_fields = ordering_fields.split(',')
            else:
                ordering_fields = []
        except:
            ordering_fields = []

        ordering_fields = ordering_fields or self._default_ordering()
        if ordering_fields:
            self.qs = self.qs.order_by(*ordering_fields)
        return self.qs


class JsonFilterBackend(BaseBackend):
    __doc__ = '\n    Allows custom filtration with json_filter GET parameter.\n    For example:\n\n        GET ?json_filters={"name": "blablabla"}\n\n    will filter queryset in this way:\n\n        .filter(__raw__={"name": "blablabla"})\n\n    You can manage filter logig with Resource attribute update_json_filter which accepts\n    (json_filter)->new_json_filter\n\n    '

    def filter(self):
        try:
            json_filter = self.request.args.get('json_filters')
            json_filter = json.loads(json_filter)
        except:
            return self.qs

        if hasattr(self.resource, 'update_json_filter'):
            json_filter = self.resource.__class__.update_json_filter(json_filter)
        self.qs = self.qs.filter(__raw__=json_filter)
        return self.qs


class SearchFilterBackend(BaseBackend):
    __doc__ = '\n    Allows custom filtration with search GET parameter.\n    For example:\n\n        GET ?search="search text"\n\n    will filter queryset in this way:\n\n        .filter(__raw__={"$text": {"$search": search_text}})\n\n    '

    def filter(self):
        try:
            search_text = self.request.args.get('search')
        except:
            search_text = ''

        if search_text:
            self.qs = self.qs.filter(__raw__={'$text': {'$search': search_text}})
        return self.qs