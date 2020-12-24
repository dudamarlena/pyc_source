# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/views.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2263 bytes
from mediagoblin import mg_globals
from mediagoblin.db.models import MediaEntry
from mediagoblin.tools.pagination import Pagination
from mediagoblin.tools.pluginapi import hook_handle
from mediagoblin.tools.response import render_to_response, render_404
from mediagoblin.decorators import uses_pagination, user_not_banned

@user_not_banned
@uses_pagination
def default_root_view(request, page):
    cursor = request.db.query(MediaEntry).filter_by(state='processed').order_by(MediaEntry.created.desc())
    pagination = Pagination(page, cursor)
    media_entries = pagination()
    return render_to_response(request, 'mediagoblin/root.html', {'media_entries': media_entries,  'allow_registration': mg_globals.app_config['allow_registration'], 
     'pagination': pagination})


def root_view(request):
    """
    Proxies to the real root view that's displayed
    """
    view = hook_handle('frontpage_view') or default_root_view
    return view(request)


def simple_template_render(request):
    """
    A view for absolutely simple template rendering.
    Just make sure 'template' is in the matchdict!
    """
    template_name = request.matchdict['template']
    return render_to_response(request, template_name, {})


def terms_of_service(request):
    if mg_globals.app_config['show_tos'] is False:
        return render_404(request)
    return render_to_response(request, 'mediagoblin/terms_of_service.html', {})