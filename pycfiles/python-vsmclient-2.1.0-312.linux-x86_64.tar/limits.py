# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/limits.py
# Compiled at: 2016-06-13 14:11:03
from vsmclient import base

class Limits(base.Resource):
    """A collection of RateLimit and AbsoluteLimit objects"""

    def __repr__(self):
        return '<Limits>'

    @property
    def absolute(self):
        for name, value in self._info['absolute'].items():
            yield AbsoluteLimit(name, value)

    @property
    def rate(self):
        for group in self._info['rate']:
            uri = group['uri']
            regex = group['regex']
            for rate in group['limit']:
                yield RateLimit(rate['verb'], uri, regex, rate['value'], rate['remaining'], rate['unit'], rate['next-available'])


class RateLimit(object):
    """Data model that represents a flattened view of a single rate limit"""

    def __init__(self, verb, uri, regex, value, remain, unit, next_available):
        self.verb = verb
        self.uri = uri
        self.regex = regex
        self.value = value
        self.remain = remain
        self.unit = unit
        self.next_available = next_available

    def __eq__(self, other):
        return self.uri == other.uri and self.regex == other.regex and self.value == other.value and self.verb == other.verb and self.remain == other.remain and self.unit == other.unit and self.next_available == other.next_available

    def __repr__(self):
        return '<RateLimit: method=%s uri=%s>' % (self.method, self.uri)


class AbsoluteLimit(object):
    """Data model that represents a single absolute limit"""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return self.value == other.value and self.name == other.name

    def __repr__(self):
        return '<AbsoluteLimit: name=%s>' % self.name


class LimitsManager(base.Manager):
    """Manager object used to interact with limits resource"""
    resource_class = Limits

    def get(self):
        """
        Get a specific extension.

        :rtype: :class:`Limits`
        """
        return self._get('/limits', 'limits')