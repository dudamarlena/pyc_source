# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudfront/invalidation.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 8106 bytes
import uuid
from boto.compat import urllib
from boto.resultset import ResultSet

class InvalidationBatch(object):
    __doc__ = 'A simple invalidation request.\n        :see: http://docs.amazonwebservices.com/AmazonCloudFront/2010-08-01/APIReference/index.html?InvalidationBatchDatatype.html\n    '

    def __init__(self, paths=None, connection=None, distribution=None, caller_reference=''):
        """Create a new invalidation request:
            :paths: An array of paths to invalidate
        """
        self.paths = paths or []
        self.distribution = distribution
        self.caller_reference = caller_reference
        if not self.caller_reference:
            self.caller_reference = str(uuid.uuid4())
        if distribution:
            self.connection = distribution
        else:
            self.connection = connection

    def __repr__(self):
        return '<InvalidationBatch: %s>' % self.id

    def add(self, path):
        """Add another path to this invalidation request"""
        return self.paths.append(path)

    def remove(self, path):
        """Remove a path from this invalidation request"""
        return self.paths.remove(path)

    def __iter__(self):
        return iter(self.paths)

    def __getitem__(self, i):
        return self.paths[i]

    def __setitem__(self, k, v):
        self.paths[k] = v

    def escape(self, p):
        """Escape a path, make sure it begins with a slash and contains no invalid characters. Retain literal wildcard characters."""
        if not p[0] == '/':
            p = '/%s' % p
        return urllib.parse.quote(p, safe='/*')

    def to_xml(self):
        """Get this batch as XML"""
        assert self.connection is not None
        s = '<?xml version="1.0" encoding="UTF-8"?>\n'
        s += '<InvalidationBatch xmlns="http://cloudfront.amazonaws.com/doc/%s/">\n' % self.connection.Version
        for p in self.paths:
            s += '    <Path>%s</Path>\n' % self.escape(p)

        s += '    <CallerReference>%s</CallerReference>\n' % self.caller_reference
        s += '</InvalidationBatch>\n'
        return s

    def startElement(self, name, attrs, connection):
        if name == 'InvalidationBatch':
            self.paths = []

    def endElement(self, name, value, connection):
        if name == 'Path':
            self.paths.append(value)
        else:
            if name == 'Status':
                self.status = value
            else:
                if name == 'Id':
                    self.id = value
                else:
                    if name == 'CreateTime':
                        self.create_time = value
                    elif name == 'CallerReference':
                        self.caller_reference = value


class InvalidationListResultSet(object):
    __doc__ = '\n    A resultset for listing invalidations on a given CloudFront distribution.\n    Implements the iterator interface and transparently handles paging results\n    from CF so even if you have many thousands of invalidations on the\n    distribution you can iterate over all invalidations in a reasonably\n    efficient manner.\n    '

    def __init__(self, markers=None, connection=None, distribution_id=None, invalidations=None, marker='', next_marker=None, max_items=None, is_truncated=False):
        self.markers = markers or []
        self.connection = connection
        self.distribution_id = distribution_id
        self.marker = marker
        self.next_marker = next_marker
        self.max_items = max_items
        self.auto_paginate = max_items is None
        self.is_truncated = is_truncated
        self._inval_cache = invalidations or []

    def __iter__(self):
        """
        A generator function for listing invalidation requests for a given
        CloudFront distribution.
        """
        conn = self.connection
        distribution_id = self.distribution_id
        result_set = self
        for inval in result_set._inval_cache:
            yield inval

        if not self.auto_paginate:
            return
        while result_set.is_truncated:
            result_set = conn.get_invalidation_requests(distribution_id, marker=result_set.next_marker, max_items=result_set.max_items)
            for i in result_set._inval_cache:
                yield i

    def startElement(self, name, attrs, connection):
        for root_elem, handler in self.markers:
            if name == root_elem:
                obj = handler(connection, distribution_id=self.distribution_id)
                self._inval_cache.append(obj)
                return obj

    def endElement(self, name, value, connection):
        if name == 'IsTruncated':
            self.is_truncated = self.to_boolean(value)
        else:
            if name == 'Marker':
                self.marker = value
            else:
                if name == 'NextMarker':
                    self.next_marker = value
                elif name == 'MaxItems':
                    self.max_items = int(value)

    def to_boolean(self, value, true_value='true'):
        if value == true_value:
            return True
        else:
            return False


class InvalidationSummary(object):
    __doc__ = '\n    Represents InvalidationSummary complex type in CloudFront API that lists\n    the id and status of a given invalidation request.\n    '

    def __init__(self, connection=None, distribution_id=None, id='', status=''):
        self.connection = connection
        self.distribution_id = distribution_id
        self.id = id
        self.status = status

    def __repr__(self):
        return '<InvalidationSummary: %s>' % self.id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Id':
            self.id = value
        elif name == 'Status':
            self.status = value

    def get_distribution(self):
        """
        Returns a Distribution object representing the parent CloudFront
        distribution of the invalidation request listed in the
        InvalidationSummary.

        :rtype: :class:`boto.cloudfront.distribution.Distribution`
        :returns: A Distribution object representing the parent CloudFront
                  distribution  of the invalidation request listed in the
                  InvalidationSummary
        """
        return self.connection.get_distribution_info(self.distribution_id)

    def get_invalidation_request(self):
        """
        Returns an InvalidationBatch object representing the invalidation
        request referred to in the InvalidationSummary.

        :rtype: :class:`boto.cloudfront.invalidation.InvalidationBatch`
        :returns: An InvalidationBatch object representing the invalidation
                  request referred to by the InvalidationSummary
        """
        return self.connection.invalidation_request_status(self.distribution_id, self.id)