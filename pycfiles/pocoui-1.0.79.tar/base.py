# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/xapian/base.py
# Compiled at: 2006-12-26 17:18:03
__doc__ = '\n    pocoo.pkg.xapian.base\n    ~~~~~~~~~~~~~~~~~~~~~\n\n    :copyright: 2006 by Christoph Hack.\n    :license: GNU GPL, see LICENSE for more details.\n'
from pocoo.application import Page, LinkableMixin
from pocoo.http import Response, TemplateResponse
from pocoo.template import PagePublisher
from pocoo.utils.form import Form, TextField
from pocoo.utils.validators import isNotEmpty
from pocoo.db import meta
from pocoo.pkg.core import db
from index import Index

class XapianSearchHandler(Page, PagePublisher, LinkableMixin):
    __module__ = __name__
    page_name = 'search'
    relative_url = 'search/'
    handler_regexes = ['search/$']

    def handle_request(self, req):
        form = Form(req, self, 'POST', TextField('keywords', validator=isNotEmpty()))
        if req.method == 'POST':
            form.update(req.form, prefix='s_')
            if not form.has_errors:
                idx = Index(req.ctx)
                qry = form.to_dict()['keywords']
                posts = idx.search(req, str(qry))
                print posts
                context = {'threads': posts, 'query': qry}
                return TemplateResponse('results.html', **context)
        context = {'form': form.generate(prefix='s_')}
        return TemplateResponse('search.html', **context)