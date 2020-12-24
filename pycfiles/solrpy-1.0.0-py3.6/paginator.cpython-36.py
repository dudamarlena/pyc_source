# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solr/paginator.py
# Compiled at: 2020-05-13 01:57:27
# Size of source mod 2**32: 4119 bytes
import math

class SolrPaginator:
    __doc__ = "\n    Create a Django-like Paginator for a solr response object. Can be handy\n    when you want to hand off a Paginator and/or Page to a template to\n    display results, and provide links to next page, etc.\n\n    For example:\n    >>> from solr import SolrConnection, SolrPaginator\n    >>>\n    >>> conn = SolrConnection('http://localhost:8083/solr')\n    >>> response = conn.query('title:huckleberry')\n    >>> paginator = SolrPaginator(response)\n    >>> print paginator.num_pages\n    >>> page = paginator.get_page(5)\n\n    For more details see the Django Paginator documentation and solrpy\n    unittests.\n\n      http://docs.djangoproject.com/en/dev/topics/pagination/\n\n    "

    def __init__(self, result, default_page_size=None):
        self.params = result._params
        self.result = result
        self.query = result._query
        if 'rows' in self.params:
            self.page_size = int(self.params['rows'])
        else:
            if default_page_size:
                try:
                    self.page_size = int(default_page_size)
                except ValueError:
                    raise ValueError('default_page_size must be an integer')

                if self.page_size < len(self.result.results):
                    raise ValueError('Invalid default_page_size specified, lower than number of results')
            else:
                self.page_size = len(self.result.results)

    @property
    def count(self):
        return int(self.result.numFound)

    @property
    def num_pages(self):
        if self.count == 0:
            return 0
        else:
            return int(math.ceil(float(self.count) / float(self.page_size)))

    @property
    def page_range(self):
        """List the index numbers of the available result pages."""
        if self.count == 0:
            return []
        else:
            return range(1, self.num_pages + 1)

    def _fetch_page(self, start=0):
        """Retrieve a new result response from Solr."""
        new_params = {}
        for k, v in self.params.items():
            new_params[str(k)] = v

        new_params['start'] = start
        return (self.query)(**new_params)

    def page(self, page_num=1):
        """Return the requested Page object"""
        try:
            int(page_num)
        except:
            raise 'PageNotAnInteger'

        if page_num not in self.page_range:
            raise EmptyPage('That page does not exist.')
        start = (page_num - 1) * self.page_size
        new_result = self._fetch_page(start=start)
        return SolrPage(new_result.results, page_num, self)


class SolrPage:
    __doc__ = 'A single Paginator-style page.'

    def __init__(self, result, page_num, paginator):
        self.result = result
        self.number = page_num
        self.paginator = paginator

    @property
    def object_list(self):
        return self.result

    def has_next(self):
        if self.number < self.paginator.num_pages:
            return True
        else:
            return False

    def has_previous(self):
        if self.number > 1:
            return True
        else:
            return False

    def has_other_pages(self):
        if self.paginator.num_pages > 1:
            return True
        else:
            return False

    def start_index(self):
        return (self.number - 1) * self.paginator.page_size

    def end_index(self):
        return self.start_index() + len(self.result) - 1

    def next_page_number(self):
        return self.number + 1

    def previous_page_number(self):
        return self.number - 1


class EmptyPage(Exception):
    pass