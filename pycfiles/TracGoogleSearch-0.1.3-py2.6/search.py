# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tracext/google/search/search.py
# Compiled at: 2008-09-03 14:35:55
import re
from genshi.filters.transform import Transformer
from trac.core import Component, implements
from trac.web import IRequestHandler
from trac.web.api import ITemplateStreamFilter
from trac.web.chrome import Chrome

class AdsenseForSearch(Component):
    config = env = log = None
    implements(ITemplateStreamFilter, IRequestHandler)

    def filter_stream(self, req, method, filename, stream, data):
        if not self.config.getbool('google.search', 'google_search_active', True):
            self.log.debug('Google search disabled. Returning regular stream.')
            return stream
        else:
            search_form_id = self.config.get('google.search', 'search_form_id', 'search')
            forid = self.config.get('google.search', 'search_form_forid', None)
            client_id = self.config.get('google.search', 'search_form_client_id', None)
            if not search_form_id:
                self.log.warn('The value of the search form id is empty. Returning regular template stream')
                return stream
            if not forid:
                self.log.warn('The value of "FORID" for the search form is empty. Returning regular template stream')
                return stream
            if not client_id:
                self.log.warn('The value of "Client ID" for the search form is empty. Returning regular template stream')
                return stream
            template = Chrome(self.env).load_template('google_search_form.html')
            data = dict(req=req, search_form_id=search_form_id, input_width=self.config.get('google.search', 'search_form_text_input_width', 31), charset=self.config.get('trac', 'default_charset', 'utf-8'), forid=forid, client_id=client_id)
            return stream | Transformer('//div/form[@id="%s"]' % search_form_id).replace(template.generate(**data))

    def match_request(self, req):
        return re.match('/gsearch/?', req.path_info) is not None

    def process_request(self, req):
        data = dict(iframe_initial_width=self.config.getint('google.search', 'iframe_initial_width'))
        return ('google_search_results.html', data, None)