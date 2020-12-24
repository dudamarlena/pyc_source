# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jlin/virtualenvs/django-rest-framework-queryset/lib/python3.7/site-packages/rest_framework_queryset/queryset.py
# Compiled at: 2019-05-08 21:33:22
# Size of source mod 2**32: 3524 bytes
from __future__ import unicode_literals
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator
import requests, copy

class BaseAPIQuerySet(object):

    def __init__(self, url, *args, **kwargs):
        _req_session = requests.Session()
        self.request_method = _req_session.get
        self.url = url
        self.args = args
        self.kwargs = kwargs

    def _call_api(self):
        """
        perform api call
        """
        return (self.request_method)(self.url, *(self.args), **self.kwargs)

    def __iter__(self):
        return iter(self.get_result())

    def __len__(self):
        return self.count()

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.get_result()[index]
        if isinstance(index, slice):
            return self.page_result(index)

    def _clone(self):
        kwargs = copy.deepcopy(self.kwargs)
        args = copy.deepcopy(self.args)
        url = copy.copy(self.url)
        cloned = (self.__class__)(url, *args, **kwargs)
        cloned.request_method = self.request_method
        return cloned

    def count(self):
        raise NotImplementedError()

    def filter(self, **kargs):
        raise NotImplementedError()

    def all(self, **kargs):
        raise NotImplementedError()

    def get_result(self):
        raise NotImplementedError()

    def page_result(self):
        raise NotImplementedError()


class RestFrameworkQuerySet(BaseAPIQuerySet):
    page_size = 100

    def __init__(self, *args, **kwargs):
        (super(RestFrameworkQuerySet, self).__init__)(*args, **kwargs)
        self._RestFrameworkQuerySet__id = None

    def __iter__(self):
        paginator = Paginator(self, self.page_size)
        for page in paginator.page_range:
            for item in paginator.page(page).object_list:
                yield item

    def _clone(self):
        cloned = super(RestFrameworkQuerySet, self)._clone()
        cloned.page_size = self.page_size
        return cloned

    def _call_api(self):
        if self._RestFrameworkQuerySet__id:
            self.url = '{}/{}/'.format(self.url.rstrip('/'), self._RestFrameworkQuerySet__id)
        return super(RestFrameworkQuerySet, self)._call_api()

    def count(self):
        cloned = self._clone()
        params = cloned.kwargs.get('params', {})
        params['offset'] = 0
        params['limit'] = 0
        resp = cloned._call_api()
        result = resp.json()
        return result['count']

    def get_result(self):
        response = self._call_api()
        result = response.json()
        if 'results' in result:
            return result['results']
        return result

    def page_result(self, slicer):
        cloned = self._clone()
        params = cloned.kwargs.setdefault('params', {})
        params['offset'] = slicer.start
        params['limit'] = slicer.stop - slicer.start
        return cloned.get_result()

    def filter(self, **kwargs):
        cloned = self._clone()
        params = cloned.kwargs.setdefault('params', {})
        params.update(kwargs)
        return cloned

    def get(self, _RestFrameworkQuerySet__id=None, **kwargs):
        cloned = (self.filter)(**kwargs)
        cloned._RestFrameworkQuerySet__id = _RestFrameworkQuerySet__id
        result = cloned.get_result()
        if isinstance(result, list):
            if len(result) > 1:
                raise MultipleObjectsReturned('get() returned more than one result, it returned {}'.format(cloned.count()))
            return result[0]
        return result

    def all(self):
        return self._clone()