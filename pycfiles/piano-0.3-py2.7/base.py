# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\lib\base.py
# Compiled at: 2012-03-22 08:36:44
"""
:mod:`piano.libs.base`
----------------------

.. autoclass:: ContextBase
   :members:
   
.. autoclass:: DocumentBase

"""
from piano.resources import interfaces as i
from mongokit import Document
from pyramid.traversal import find_interface, find_root

class ContextBase(dict):
    """ Base (abstract) class for all resources (contexts).
    """
    __name__ = None
    __parent__ = None
    __app__ = None
    __site__ = None

    def __init__(self, key=None, parent=None, **kwargs):
        self.__name__ = key
        self.__parent__ = parent
        self.request = find_root(self).request
        self.__app__ = find_interface(self, i.IApp)
        self.__site__ = find_interface(self, i.ISite)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def appname(self):
        """Returns the name of the application.  
        """
        return self.__app__.__name__

    @property
    def sitename(self):
        """Returns the name of the site.  
        """
        return self.__site__.__name__

    def get_conn(self, app=None, site=None):
        """Returns a raw MongoDB connection.  If none of the arguments are
        set it will try to configure the connection based on the instances 
        app and site name.  Otherwise, it is up to you to choose the
        database and collection to use.
        """
        mongo_conn = self.request.conn
        if app is None and site is None:
            return mongo_conn[self.appname][self.sitename]
        else:
            if app is not None:
                mongo_conn = mongo_conn[app]
            if site is not None:
                mongo_conn = mongo_conn[site]
            return mongo_conn


class DocumentBase(Document):
    """ Base (abstract) class for all documents (MongoDB).
    """
    use_dot_notation = False
    use_schemaless = False
    skip_validation = False