# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/internal_warnings.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import functools, six
from collections import defaultdict
from rest_framework.response import Response
from sentry.api.base import Endpoint
from sentry.api.permissions import SuperuserPermission
from sentry.utils.warnings import DeprecatedSettingWarning, UnsupportedBackend, seen_warnings

class InternalWarningsEndpoint(Endpoint):
    permission_classes = (
     SuperuserPermission,)

    def get(self, request):
        groupings = {DeprecatedSettingWarning: 'Deprecated Settings', 
           UnsupportedBackend: 'Unsupported Backends'}
        groups = defaultdict(list)
        warnings = []
        for warning in seen_warnings:
            cls = type(warning)
            if cls in groupings:
                groups[cls].append(six.text_type(warning))
            else:
                warnings.append(six.text_type(warning))

        sort_by_message = functools.partial(sorted, key=six.binary_type)
        data = {'groups': sorted([ (groupings[key], sort_by_message(values)) for key, values in groups.items() ]), 
           'warnings': sort_by_message(warnings)}
        return Response(data)