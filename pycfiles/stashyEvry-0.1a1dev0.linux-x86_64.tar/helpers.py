# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/e210990/bin/python26/lib/python2.6/site-packages/stashy/helpers.py
# Compiled at: 2014-06-25 10:41:27
from .errors import maybe_throw

def add_json_headers(kw):
    if 'headers' not in kw:
        kw['headers'] = {}
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    for (header, value) in headers.items():
        kw['headers'][header] = value

    return kw


class ResourceBase(object):

    def __init__(self, url, client, parent):
        self._url = url
        self._client = client
        self._parent = parent

    def url(self, resource_url=''):
        if resource_url and not resource_url.startswith('/'):
            resource_url = '/' + resource_url
        if self._url.endswith('/'):
            url = self._url[:-1]
        else:
            url = self._url
        return url + resource_url

    def paginate(self, resource_url, params=None):
        url = self.url(resource_url)
        more = True
        start = None
        while more:
            kw = {}
            if params:
                kw['params'] = params
            if start is not None:
                kw['params'] = dict(start=start)
            response = self._client.get(url, **kw)
            maybe_throw(response)
            data = response.json()
            if 'values' not in data:
                return
            for item in data['values']:
                yield item

            if data['isLastPage']:
                more = False
            else:
                more = True
                start = data['nextPageStart']

        return


class IterableResource(object):

    def __iter__(self):
        """
        Convenience method around self.all()
        """
        return self.all()

    def all(self):
        """
        Retrieve all the resources.
        """
        return self.paginate('')

    def list(self):
        """
        Convenience method to return a list (rather than iterable) of all elements
        """
        return list(self.all())


class FilteredIterableResource(IterableResource):

    def all(self, filter=None):
        """
        Retrieve all the resources, optionally modified by filter.
        """
        params = {}
        if filter:
            params['filter'] = filter
        return self.paginate('', params)

    def list(self, filter=None):
        """
        Convenience method to return a list (rather than iterable) of all elements
        """
        return list(self.all(filter))


class Nested(object):

    def __init__(self, cls, relative_path=None):
        if relative_path:
            if not relative_path.startswith('/'):
                relative_path = '/' + relative_path
            self.relative_path = relative_path
        else:
            self.relative_path = '/%s' % cls.__name__.lower()
        self.cls = cls

    def __get__(self, instance, kind):
        parent_url = instance._url
        if parent_url.endswith('/'):
            parent_url = parent_url[:-1]
        url = parent_url + self.relative_path
        return self.cls(url=url, client=instance._client, parent=instance)