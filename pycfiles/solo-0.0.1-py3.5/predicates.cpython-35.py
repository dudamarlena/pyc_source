# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/configurator/config/predicates.py
# Compiled at: 2016-03-06 14:41:25
# Size of source mod 2**32: 879 bytes
from .util import as_sorted_tuple

class RequestMethodPredicate(object):

    def __init__(self, val, config):
        """
        :param val: value passed to view_config/view_defaults
        :param config:
        """
        request_method = as_sorted_tuple(val)
        if 'GET' in request_method and 'HEAD' not in request_method:
            request_method = as_sorted_tuple(request_method + ('HEAD', ))
        self.val = request_method

    def text(self):
        return 'request_method = %s' % ','.join(self.val)

    phash = text

    def __call__(self, context, request):
        """
        :param context: at the moment context may be only None
        :type context: None
        :param: request: Django request object
        :type request: :class:`django.http.HttpRequest`
        """
        return request.method in self.val