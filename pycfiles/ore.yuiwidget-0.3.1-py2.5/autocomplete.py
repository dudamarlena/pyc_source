# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/yuiwidget/autocomplete.py
# Compiled at: 2008-12-18 21:39:01
"""
Autocomplete widgets

  ISourceQueryable
  SourceQueryView
  
  SourceQueryJSON

  Site Source AutoCompletes

  Context Source Auto Completes

    
$Id: $
"""
from zope.app.form.browser import itemswidgets, textwidgets, interfaces
from zope import interface
from zc.resourcelibrary import need
from ore.alchemist import model, Session
import simplejson

class AutoComplete(object):
    source = None


class SiteSourceQueryView(object):
    interface.implements(interfaces.ISourceQueryView)
    template = '\n    <div id="%(name)s.autofield">\n       <input id="%(name)s" type="text">\n       <div id="%(name)s.autodiv">\n       </div>\n    </div>\n    \n    <script type="text/javascript">\n      \n      search_schema = var mySchema2 = ["ResultItem", "KeyDataField"];\n      data_source = new YAHOO.widget.DS_XHR("%(source_url)s", search_schema; \n    </script>\n    '
    source_view = ''
    columns = None
    config = {}

    def render(self, name):
        need('yui-autocomplete')
        ns = {}
        ns.update(self.config)
        ns['search_url'] = self.search_url
        ns['name'] = self.name + '.searchstring'
        return self.template % ns

    @property
    def item_field_mapping(self):
        domain_interface = model.queryModelInterface(self.context.domain_model)
        schema.getFields(domain_interface)

    @property
    def search_url(self):
        url = absoluteURL(self.context, self.request)
        return url + self.search_view

    def results(self):
        return []


class SourceQueryJSON(object):
    """a view providing json (results) of querying sources
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.queryable = ISourceQuery(context)

    def __call__(self):
        query_term = self.request.get('query')
        if not query_term:
            return simplejson.dumps([])
        results = self.queryable.query(query_term)
        return simplejson.dumps([])


class TextColumnSourceQuery(object):
    interface.implements(interfaces.ISourceQuery)

    def __init__(self, context, column_name):
        self.context
        self.column_name = column_name

    def query(self, term):
        domain_model = self.context.domain_model
        results = Session().query(domain_model).filter(domain_model.c[self.column_name].like('\\%s%s\\%' % term).all())
        return results


class ISourceQuery(interface.Interface):

    def query(search_term):
        """
        query a source for a search term
        """
        pass

    def hasTerm(term):
        """
        verify the existence of a term
        """
        pass