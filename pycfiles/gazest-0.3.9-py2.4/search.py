# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/controllers/search.py
# Compiled at: 2007-10-26 05:13:22
import logging
from gazest.lib.base import *
log = logging.getLogger(__name__)

class SearchController(BaseController):
    __module__ = __name__

    def results(self):
        c.noindex = True
        c.search_term = request.params['term']
        c.title = "Search results for '%s'" % c.search_term
        clauses = [ RevNode.body.like('%%%s%%' % word) for word in c.search_term.split() ]
        q = Page.query.join('rev').filter(model.and_(*clauses))
        c.pages = list(q.limit(50))
        return render('/search_results.mako')