# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_table/views.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 569 bytes
from django.http import HttpRequest, JsonResponse
from . import utils

def get_table_choices(request: HttpRequest) -> JsonResponse:
    """
    After choosing table, form has to show available columns. It's done
    by JavaScript to call this view to get that data. URL expect one
    GET parameter called ``table``. It's because it's easier to dynamicly
    change in JavaScript.

    Output format is same as from :any:`cms_qe_table.utils.get_table_choices`.
    """
    table = request.GET.get('table', '')
    return JsonResponse(utils.get_table_choices(table))