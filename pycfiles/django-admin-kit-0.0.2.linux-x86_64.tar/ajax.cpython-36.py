# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rohan/Django/django-admin-kit/.venv/lib/python3.6/site-packages/tests/test_ajax_duplicate/ajax.py
# Compiled at: 2017-12-06 08:53:02
# Size of source mod 2**32: 534 bytes
import admin_kit

class GenresAjax(admin_kit.ajax.Ajax):
    unique = True

    def run(self, request):
        query = request.GET.getlist('q[]')
        response = list(zip(query, query))
        return response


class GenresDescriptionAjax(admin_kit.ajax.Ajax):
    response_type = 'text'

    def run(self, request):
        query = request.GET['q']
        if query:
            return 'Description of %s' % str(query)


admin_kit.site.register('genres-desc', GenresDescriptionAjax)
admin_kit.site.register('genres', GenresAjax)