# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tracext/sphinx/main.py
# Compiled at: 2009-07-31 20:01:00
"""
"""
import os
from genshi import XML
from trac.core import *
from trac.web.chrome import INavigationContributor, ITemplateProvider, add_stylesheet
from trac.web.main import IRequestHandler
from trac.util import escape, Markup
from sphinx.webtools import update_docs, reformat_content_links, PicklerContentManager, get_genentries, get_modentries
from sphinx.webtools import highlight, search

class SphinxPlugin(Component):
    implements(INavigationContributor, IRequestHandler, ITemplateProvider)

    def get_active_navigation_item(self, req):
        """
        """
        return 'sphinx'

    def get_navigation_items(self, req):
        """
        """
        try:
            navbar_title = self.config['sphinx'].get('navbar_title')
            if not navbar_title or navbar_title == '':
                navbar_title = 'Doc Sphinx'
        except:
            pass

        yield (
         'mainnav', 'sphinx',
         Markup('<a href="%s">%s</a>' % (
          self.env.href.sphinx(), navbar_title)))

    def match_request(self, req):
        """
        """
        return req.path_info == '/sphinx'

    def process_request(self, req):
        """
        """
        add_stylesheet(req, 'static/css/sphinx.css')
        try:
            search_words = req.args.get('search')
            if not search_words == '':
                return self.__search(search_words)
        except:
            pass

        action = req.args.get('action')
        item = req.args.get('item')
        if action == 'refresh':
            return self.__refresh()
        if action == 'index' or item == 'genindex':
            return self.__index()
        if action == 'modules' or item == 'modindex':
            return self.__modules()
        if action == 'search' or item == 'search':
            return self.__search()
        pickler_url = req.args.get('item')
        search_words = req.args.get('search_words')
        return self.__view(pickler_url, search_words)

    def __get_source_dir(self):
        """
        """
        try:
            source_dir = self.config['sphinx'].get('source_dir')
            if source_dir or not source_dir == '':
                return source_dir
        except:
            pass

        project_dir = self.config['trac'].get('repository_dir')
        source_dir = os.path.join(project_dir, 'docs', 'source')
        return source_dir

    def __get_doc_dir(self):
        """
        """
        try:
            doc_dir = self.config['sphinx'].get('doc_dir')
            if doc_dir or not doc_dir == '':
                return doc_dir
        except:
            pass

        trac_dir = self.env.path
        doc_dir = os.path.join(trac_dir, 'sphinx-docs')
        return doc_dir

    def __refresh(self):
        """Controller for sphinx pickle doc refresh.
        """
        source_dir = self.__get_source_dir()
        doc_dir = self.__get_doc_dir()
        error = update_docs(source_dir=source_dir, doc_dir=doc_dir)
        if not error:
            msg = '<h1>'
            msg += '<a href="/pygloo/sphinx">Update done successfully!</a>'
            msg += '</h1>'
        else:
            msg = '<h1>An error occurred during the built!</h1>'
        result = dict(toc=None, rellinks=None, search='', content=XML(msg), error=error)
        return (
         'sphinx-view.html', result, None)

    def __view(self, pickler_url=None, search_words=None):
        """
        """
        base_url = 'sphinx'
        doc_dir = self.__get_doc_dir()
        if not pickler_url:
            pickler_url = 'index'
        pickler_ct_manager = PicklerContentManager(base_url, doc_dir, pickler_url)
        toc_str = pickler_ct_manager.get_toc()
        if toc_str:
            toc = XML(toc_str)
        else:
            toc = None
        rellinks = pickler_ct_manager.get_rellinks()
        content_str = pickler_ct_manager.get_body()
        if search_words and content_str:
            search_words = search_words.replace('+', ' ')
            content_str = highlight(content_str, search_words)
        if content_str:
            content_xml = XML(content_str)
            content = reformat_content_links(base_url, doc_dir, content_xml)
        else:
            content = None
        result = dict(toc=toc, rellinks=rellinks, search='', content=content, error=None)
        return (
         'sphinx-view.html', result, None)

    def __index(self):
        """Controller for genindex sphinx function.
        """
        base_url = 'sphinx'
        doc_dir = self.__get_doc_dir()
        entries = get_genentries(base_url, doc_dir)
        result = dict(search='', entries=entries)
        return (
         'sphinx-index.html', result, None)

    def __modules(self):
        """Controller for modindex sphinx function.
        """
        base_url = 'sphinx'
        doc_dir = self.__get_doc_dir()
        entries = get_modentries(base_url, doc_dir)
        result = dict(search='', entries=entries)
        return (
         'sphinx-modules.html', result, None)

    def __search(self, search_words=''):
        """Controller for the search sphinx function
        """
        base_url = 'sphinx'
        doc_dir = self.__get_doc_dir()
        if not search_words == '':
            result = search(base_url, doc_dir, search_words)
        else:
            result = None
        result = dict(search=search_words, result=result)
        return (
         'sphinx-search.html', result, None)

    def get_templates_dirs(self):
        """Used to add the plugin's templates.
        """
        from pkg_resources import resource_filename
        return [
         resource_filename(__name__, 'templates')]

    def get_htdocs_dirs(self):
        """Used to add the plugin's htdocs.
        """
        from pkg_resources import resource_filename
        return [
         (
          'static', resource_filename(__name__, 'htdocs'))]