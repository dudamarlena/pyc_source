# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\views\apps.py
# Compiled at: 2012-03-22 14:36:39
"""General Views

:mod:`piano.views.apps`
-----------------------

.. autofunction:: dashboard

"""
from piano.resources import contexts as ctx
from pyramid.view import view_config

@view_config(context=ctx.App, renderer='piano.web.templates.app:dashboard.mako')
def dashboard(context, request):
    """Renders a list of sites available to this application.
    """
    page_title = 'Dashboard'
    new_site_url = request.resource_url(context, 'new-site')
    site_list = context.list_sites()
    return dict(app_title=page_title, sites=site_list, page_title=page_title, new_site_url=new_site_url)