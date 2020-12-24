# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gint/Dokumenty/report/app/templado/templatetags/search_form.py
# Compiled at: 2015-02-24 07:32:16
from bootstrap3.forms import render_form
from django import template
from ..forms import SearchForm
register = template.Library()

@register.simple_tag()
def bootstrap_query_form(request):
    if request.GET.get('q'):
        form = SearchForm(request.GET)
    else:
        form = SearchForm()
    return render_form(form, layout='inline')