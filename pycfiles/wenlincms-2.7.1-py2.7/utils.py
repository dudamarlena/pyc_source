# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/boot/updates/contrib/comments/views/utils.py
# Compiled at: 2016-05-20 23:42:08
"""
A few bits of helper functions for comment views.
"""
import textwrap
from django.contrib import comments
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, resolve_url
from django.template import RequestContext
from django.utils.http import is_safe_url
from django.utils.six.moves.urllib.parse import urlencode

def next_redirect(request, fallback, **get_kwargs):
    """
    Handle the "where should I go next?" part of comment views.

    The next value could be a
    ``?next=...`` GET arg or the URL of a given view (``fallback``). See
    the view modules for examples.

    Returns an ``HttpResponseRedirect``.
    """
    next = request.POST.get('next')
    if not is_safe_url(url=next, host=request.get_host()):
        next = resolve_url(fallback)
    if get_kwargs:
        if '#' in next:
            tmp = next.rsplit('#', 1)
            next = tmp[0]
            anchor = '#' + tmp[1]
        else:
            anchor = ''
        joiner = '&' if '?' in next else '?'
        next += joiner + urlencode(get_kwargs) + anchor
    return HttpResponseRedirect(next)


def confirmation_view(template, doc='Display a confirmation view.'):
    """
    Confirmation view generator for the "comment was
    posted/flagged/deleted/approved" views.
    """

    def confirmed(request):
        comment = None
        if 'c' in request.GET:
            try:
                comment = comments.get_model().objects.get(pk=request.GET['c'])
            except (ObjectDoesNotExist, ValueError):
                pass

        return render_to_response(template, {'comment': comment}, context_instance=RequestContext(request))

    confirmed.__doc__ = textwrap.dedent('        %s\n\n        Templates: :template:`%s``\n        Context:\n            comment\n                The posted comment\n        ' % (doc, template))
    return confirmed