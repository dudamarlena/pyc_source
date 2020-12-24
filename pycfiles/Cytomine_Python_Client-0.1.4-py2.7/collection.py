# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cytomine/models/collection.py
# Compiled at: 2017-09-05 05:52:58
__author__ = 'Stévens Benjamin <b.stevens@ulg.ac.be>'
__contributors__ = ['Marée Raphaël <raphael.maree@ulg.ac.be>', 'Rollus Loïc <lrollus@ulg.ac.be']
__copyright__ = 'Copyright 2010-2015 University of Liège, Belgium, http://www.cytomine.be/'
import json

class Collection(object):
    collection_identifier = 'collection'

    def __init__(self, model, params=None):
        self._model = model
        self._data = []
        self._per_page = 0
        self._page_index = 0
        self._offset = 0
        self._total = None
        self._total_pages = None
        if params:
            self.parse(params)
        return

    def __iter__(self):
        return iter(self._data)

    def parse(self, params=None):
        response = json.loads(params)
        if hasattr(self, 'collection_identifier'):
            data = response[self.collection_identifier]
            self._total = int(response['size'])
            self._offset = int(response['offset'])
            self._total_pages = int(response['totalPages'])
            self._per_page = int(response['perPage'])
            if self._per_page != 0:
                self._page_index = self._offset / self._per_page
            else:
                self._page_index = 0
        for model in data:
            self._data.append(self._model().__class__(json.dumps(model)))

    def next_page(self):
        if self._total_pages:
            if self._page_index == self._total_pages - 1:
                return
            else:
                self._page_index = self._page_index + 1
                return self._page_index

        else:
            return
        return

    def previous_page(self):
        self._per_page = max(1, self._per_page - 1)
        return self._per_page

    def get_paginator_query(self):
        return 'max=%d&offset=%d' % (self._per_page, self._page_index * self._per_page)

    def init_paginator(self, per_page, page_index=0):
        self._per_page = per_page
        self._page_index = page_index

    def data(self):
        return self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __iadd__(self, other):
        if not isinstance(other, Collection):
            raise ValueError("Only two Collection objects can be added together, 'other' is not an instance of Collection.")
        self._data.extend(other.data())
        return self

    def __add__(self, other):
        if not isinstance(other, Collection):
            raise ValueError("Only two Collection objects can be added together, 'other' is not an instance of Collection.")
        collection = Collection({})
        collection += self.data()
        collection += other
        return collection