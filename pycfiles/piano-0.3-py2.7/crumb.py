# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\lib\crumb.py
# Compiled at: 2012-03-20 09:36:41
"""
:mod:`piano.libs.crumb`
-----------------------

.. autoclass:: Breadcrumb
   :members:

"""
from pyramid.events import subscriber, NewRequest

class Breadcrumb(object):
    """ Tracks the current position within the site and creates a breadcrumb
    trail.
    """

    def __init__(self, uri=None):
        if uri:
            self.uri = uri
        else:
            self._uri = uri

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        self._protocol = 'http://'
        protocols = ['http://', 'https://', 'ftp://', 'sftp://']
        for protocol in protocols:
            if uri.startswith(protocol):
                self._protocol = protocol
                uri = uri[len(protocol):]

        self._uri = uri.rstrip('/')
        self.crumbs = self._uri.split('/')

    @property
    def links(self):
        """Returns the list of links which make up the breadcrumb at the 
        current level.
        """
        links = []
        for count, crumb in enumerate(self.crumbs, start=1):
            crumb_uri = self._protocol + ('/').join(self.crumbs[0:count])
            links.append((crumb_uri, crumb))

        return links


@subscriber(NewRequest)
def breadcrumb_subscriber(event):
    """Attaches a breadcrumb to each request.
    """
    event.request.crumb = Breadcrumb(event.request.url)