# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/code/python/libraries/respite/respite/utils/datastructures.py
# Compiled at: 2012-11-28 11:59:47
from django.conf import settings
from django.utils import simplejson as json
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_unicode
from django.http import QueryDict

class NestedQueryDict(QueryDict):
    """
    A QueryDict that allows initialization with a dictionary instead of a query string
    and facilitates for nested dictionaries.
    """

    def __init__(self, data, mutable=False, encoding=None):
        MultiValueDict.__init__(self)
        if not encoding:
            from django.conf import settings
            encoding = settings.DEFAULT_CHARSET
        self.encoding = encoding
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (list, set)):
                    self.setlistdefault(key, [])
                    items = [ NestedQueryDict(item) for item in value ]
                    super(MultiValueDict, self).__setitem__(key, items)
                elif isinstance(value, dict):
                    self.appendlist(force_unicode(key, encoding, errors='replace'), NestedQueryDict(value))
                else:
                    self.appendlist(force_unicode(key, encoding, errors='replace'), force_unicode(value, encoding, errors='replace'))

        self._mutable = mutable