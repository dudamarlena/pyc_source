# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/paginator.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
from django.conf import settings
from django.utils import six
from tastypie.exceptions import BadRequest
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

class Paginator(object):
    """
    Limits result sets down to sane amounts for passing to the client.

    This is used in place of Django's ``Paginator`` due to the way pagination
    works. ``limit`` & ``offset`` (tastypie) are used in place of ``page``
    (Django) so none of the page-related calculations are necessary.

    This implementation also provides additional details like the
    ``total_count`` of resources seen and convenience links to the
    ``previous``/``next`` pages of data as available.
    """

    def __init__(self, request_data, objects, resource_uri=None, limit=None, offset=0, max_limit=1000, collection_name=b'objects'):
        """
        Instantiates the ``Paginator`` and allows for some configuration.

        The ``request_data`` argument ought to be a dictionary-like object.
        May provide ``limit`` and/or ``offset`` to override the defaults.
        Commonly provided ``request.GET``. Required.

        The ``objects`` should be a list-like object of ``Resources``.
        This is typically a ``QuerySet`` but can be anything that
        implements slicing. Required.

        Optionally accepts a ``limit`` argument, which specifies how many
        items to show at a time. Defaults to ``None``, which is no limit.

        Optionally accepts an ``offset`` argument, which specifies where in
        the ``objects`` to start displaying results from. Defaults to 0.

        Optionally accepts a ``max_limit`` argument, which the upper bound
        limit. Defaults to ``1000``. If you set it to 0 or ``None``, no upper
        bound will be enforced.
        """
        self.request_data = request_data
        self.objects = objects
        self.limit = limit
        self.max_limit = max_limit
        self.offset = offset
        self.resource_uri = resource_uri
        self.collection_name = collection_name

    def get_limit(self):
        """
        Determines the proper maximum number of results to return.

        In order of importance, it will use:

            * The user-requested ``limit`` from the GET parameters, if specified.
            * The object-level ``limit`` if specified.
            * ``settings.API_LIMIT_PER_PAGE`` if specified.

        Default is 20 per page.
        """
        limit = self.request_data.get(b'limit', self.limit)
        if limit is None:
            limit = getattr(settings, b'API_LIMIT_PER_PAGE', 20)
        try:
            limit = int(limit)
        except ValueError:
            raise BadRequest(b"Invalid limit '%s' provided. Please provide a positive integer." % limit)

        if limit < 0:
            raise BadRequest(b"Invalid limit '%s' provided. Please provide a positive integer >= 0." % limit)
        if self.max_limit and (not limit or limit > self.max_limit):
            return self.max_limit
        else:
            return limit

    def get_offset(self):
        """
        Determines the proper starting offset of results to return.

        It attempts to use the user-provided ``offset`` from the GET parameters,
        if specified. Otherwise, it falls back to the object-level ``offset``.

        Default is 0.
        """
        offset = self.offset
        if b'offset' in self.request_data:
            offset = self.request_data[b'offset']
        try:
            offset = int(offset)
        except ValueError:
            raise BadRequest(b"Invalid offset '%s' provided. Please provide an integer." % offset)

        if offset < 0:
            raise BadRequest(b"Invalid offset '%s' provided. Please provide a positive integer >= 0." % offset)
        return offset

    def get_slice(self, limit, offset):
        """
        Slices the result set to the specified ``limit`` & ``offset``.
        """
        if limit == 0:
            return self.objects[offset:]
        return self.objects[offset:offset + limit]

    def get_count(self):
        """
        Returns a count of the total number of objects seen.
        """
        try:
            return self.objects.count()
        except (AttributeError, TypeError):
            return len(self.objects)

    def get_previous(self, limit, offset):
        """
        If a previous page is available, will generate a URL to request that
        page. If not available, this returns ``None``.
        """
        if offset - limit < 0:
            return None
        else:
            return self._generate_uri(limit, offset - limit)

    def get_next(self, limit, offset, count):
        """
        If a next page is available, will generate a URL to request that
        page. If not available, this returns ``None``.
        """
        if offset + limit >= count:
            return None
        else:
            return self._generate_uri(limit, offset + limit)

    def _generate_uri(self, limit, offset):
        if self.resource_uri is None:
            return
        else:
            try:
                request_params = self.request_data.copy()
                if b'limit' in request_params:
                    del request_params[b'limit']
                if b'offset' in request_params:
                    del request_params[b'offset']
                request_params.update({b'limit': limit, b'offset': offset})
                encoded_params = request_params.urlencode()
            except AttributeError:
                request_params = {}
                for k, v in self.request_data.items():
                    if isinstance(v, six.text_type):
                        request_params[k] = v.encode(b'utf-8')
                    else:
                        request_params[k] = v

                if b'limit' in request_params:
                    del request_params[b'limit']
                if b'offset' in request_params:
                    del request_params[b'offset']
                request_params.update({b'limit': limit, b'offset': offset})
                encoded_params = urlencode(request_params)

            return b'%s?%s' % (
             self.resource_uri,
             encoded_params)

    def page(self):
        """
        Generates all pertinent data about the requested page.

        Handles getting the correct ``limit`` & ``offset``, then slices off
        the correct set of results and returns all pertinent metadata.
        """
        limit = self.get_limit()
        offset = self.get_offset()
        count = self.get_count()
        objects = self.get_slice(limit, offset)
        meta = {b'offset': offset, 
           b'limit': limit, 
           b'total_count': count}
        if limit:
            meta[b'previous'] = self.get_previous(limit, offset)
            meta[b'next'] = self.get_next(limit, offset, count)
        return {self.collection_name: objects, 
           b'meta': meta}