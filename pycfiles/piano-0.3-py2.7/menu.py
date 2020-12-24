# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\services\menu.py
# Compiled at: 2012-03-22 14:35:44
"""
:mod:`piano.services.menu`
--------------------------

.. autoclass:: MenuService
   :members:
   
"""
from piano.resources import contexts as ctx
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPInternalServerError
import logging
logger = logging.getLogger(__name__)

@view_defaults(name='menu', context=ctx.Service, xhr=False, renderer='jsonp')
class MenuService(object):
    """A RESTful command that returns child pages of the parent page or site.
    This command assumes the url always starts with the app, then the site,
    and ends with the page (parent of the children to return).  If it is just 
    the site, then the children of the site are returned only.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.conn = request.conn
        self.url = request.GET['url']
        self.page = request.GET.setdefault('page', '')
        segments = self.url.strip('/').split('/')
        self.app = segments[0]
        self.site = segments[1]
        if self.page == '':
            self.parent = self.site
            self.page = None
        else:
            self.parent = self.page
        return

    @view_config(request_method='GET')
    def get(self):
        """Returns a dictionary of pages with links.
        
        **Site**: /services/menu?url=/my-site
            - Returns all children for my-site
            
        **Page**: /services/menu?url=/my-site&page=home
            - Returns all children for my-site/home
        """
        try:
            return self._children(self.parent, self.site, self.app)
        except:
            return HTTPInternalServerError('Request did not execute properly.')

    def _children(self, parent, site, app):
        coll = self.conn[app][site]
        children = coll.find({'parent': parent}, {'slug': 1, 'title': 1})
        r = lambda c: ('/').join([self.url, c])
        return [ dict(title=child['title'], slug=child['slug'], url=r(child['slug'])) for child in children
               ]