# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/database.py
# Compiled at: 2010-05-30 09:35:01
import sys
from werkzeug import cached_property

class Pagination(object):

    def __init__(self, query, per_page, page, endpoint):
        self.query = query
        self.per_page = per_page
        self.page = page
        self.endpoint = endpoint

    @cached_property
    def count(self):
        return self.query.count()

    @cached_property
    def entries(self):
        return self.query.offset((self.page - 1) * self.per_page).limit(self.per_page).all()

    has_previous = property(lambda x: x.page > 1)
    has_next = property(lambda x: x.page < x.pages)
    previous = property(lambda x: x.page - 1)
    next = property(lambda x: x.page + 1)
    pages = property(lambda x: max(0, x.count - 1) // x.per_page + 1)