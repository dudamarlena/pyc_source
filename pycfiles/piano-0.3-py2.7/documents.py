# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\piano\resources\documents.py
# Compiled at: 2012-03-22 14:35:21
"""
:mod:`piano.resources.documents`
--------------------------------

.. autoclass:: SiteDocument
   :members:
   
.. autoclass:: PageDocument
   :members:
   
"""
from piano.lib import base as b
from piano.lib import helpers as h
import datetime, logging
logger = logging.getLogger(__name__)

class SiteDocument(b.DocumentBase):
    """"Document representation of a site.
    """
    __database__ = None
    __collection__ = 'sites'
    structure = {'slug': str, 
       'title': unicode, 
       'description': unicode, 
       'created': datetime.datetime, 
       'views': int}
    required_fields = [
     'title',
     'slug',
     'created']
    default_values = {'views': 1, 
       'created': h.now()}


class PageData(b.DocumentBase):
    """Document for page-level data.  Page-level components need to have a
    module 'models' and a class 'PageModel' which extends this class.
    """
    structure = {}


class PageDocument(b.DocumentBase):
    """"Document representation of a page.
    """
    structure = {'title': unicode, 
       'slug': str, 
       'description': unicode, 
       'created': datetime.datetime, 
       'keywords': list, 
       'views': int, 
       'source': str, 
       'parent': str, 
       'data': PageData}
    required_fields = [
     'title',
     'slug',
     'source',
     'parent',
     'created']
    default_values = {'views': 1, 
       'title': 'Home', 
       'slug': 'home', 
       'source': 'sample.home', 
       'created': h.now()}
    use_auto_refs = True


try:
    from piano.lib.mongo import conn
    conn.register([
     PageDocument,
     SiteDocument])
except:
    pass
else:
    logging.debug('Registered Mongo documents')