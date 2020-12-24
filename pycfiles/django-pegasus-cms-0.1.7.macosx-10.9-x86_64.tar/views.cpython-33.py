# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/views.py
# Compiled at: 2015-02-18 13:07:40
# Size of source mod 2**32: 513 bytes
from __future__ import absolute_import, division
from django.core.urlresolvers import NoReverseMatch, reverse
from django.http import HttpResponseRedirect
from search.views import CeleritySearchView

def error404(request):
    return CeleritySearchView.as_view()(request, is_404=True)


def redirect404(request):
    try:
        return HttpResponseRedirect(reverse('404'))
    except NoReverseMatch as e:
        return HttpResponseRedirect(reverse('pages-root'))