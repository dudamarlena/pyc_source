# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/model_mixins.py
# Compiled at: 2017-01-12 12:04:40
# Size of source mod 2**32: 309 bytes


class DeleteManyMixin:
    _allowed_methods = [
     'delete']

    def delete(self, request):
        ids = None
        if request.json:
            ids = request.json.get('ids')
        qs = self.get_queryset()
        if ids:
            qs = qs.filter(id__in=ids)
        qs.delete()
        return '{}'