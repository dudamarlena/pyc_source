# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\views\sites.py
# Compiled at: 2012-03-22 14:36:39
"""
:mod:`piano.views.sites`
------------------------

.. autofunction:: piano.views.sites.view_site

.. autofunction:: piano.views.sites.new_site

.. autofunction:: piano.views.sites.delete_site

"""
from piano.lib import helpers as h
from piano.lib import mvc
from piano.resources import contexts as ctx
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

@view_config(context=ctx.Site, renderer='piano.web.templates.site:view.mako', request_method='GET')
def view_site(context, request):
    """Main view of the site.
    """
    add_page_url = request.resource_url(context, 'add-page')
    return mvc.PageModel(context, page_views=context.views, page_created=context.date_created, add_page_url=add_page_url)


@view_config(name='new-site', context=ctx.App, renderer='piano.web.templates.site:edit.mako', request_method='GET')
@view_config(name='new-site', context=ctx.App, request_method='POST')
def new_site(context, request):
    """Add a new site.
    """
    if 'form.submitted' in request.params:
        title = request.params['title']
        slug = str(h.urlify(title))
        site = ctx.Site(key=slug, parent=context, title=title, slug=slug).save(include_default=True)
        return HTTPFound(location=request.resource_url(context, site.__name__))
    save_site_url = request.resource_url(context, 'new-site')
    return dict(page_title='New Site', save_site_url=save_site_url)


@view_config(name='delete-site', context=ctx.Site, request_method='GET')
def delete_site(context, request):
    """Delete an existing site.
    """
    context.delete()
    return HTTPFound(location=request.resource_url(context.__parent__))