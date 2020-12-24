# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/system_options.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six, sentry
from django.conf import settings
from rest_framework.response import Response
from sentry import options
from sentry.api.base import Endpoint
from sentry.api.permissions import SuperuserPermission
from sentry.utils.email import is_smtp_enabled

class SystemOptionsEndpoint(Endpoint):
    permission_classes = (
     SuperuserPermission,)

    def get(self, request):
        query = request.GET.get('query')
        if query == 'is:required':
            option_list = options.filter(flag=options.FLAG_REQUIRED)
        else:
            if query:
                return Response(('{} is not a supported search query').format(query), status=400)
            option_list = options.all()
        smtp_disabled = not is_smtp_enabled()
        results = {}
        for k in option_list:
            disabled, disabled_reason = False, None
            if smtp_disabled and k.name[:5] == 'mail.':
                disabled_reason, disabled = 'smtpDisabled', True
            elif bool(k.flags & options.FLAG_PRIORITIZE_DISK and settings.SENTRY_OPTIONS.get(k.name)):
                disabled_reason, disabled = 'diskPriority', True
            results[k.name] = {'value': options.get(k.name), 
               'field': {'default': k.default(), 
                         'required': bool(k.flags & options.FLAG_REQUIRED), 
                         'disabled': disabled, 
                         'disabledReason': disabled_reason, 
                         'isSet': options.isset(k.name), 
                         'allowEmpty': bool(k.flags & options.FLAG_ALLOW_EMPTY)}}

        return Response(results)

    def put(self, request):
        for k, v in six.iteritems(request.data):
            if v and isinstance(v, six.string_types):
                v = v.strip()
            try:
                option = options.lookup_key(k)
            except options.UnknownOption:
                return Response({'error': 'unknown_option', 'errorDetail': {'option': k}}, status=400)

            try:
                if not option.flags & options.FLAG_ALLOW_EMPTY and not v:
                    options.delete(k)
                else:
                    options.set(k, v)
            except TypeError as e:
                return Response({'error': 'invalid_type', 
                   'errorDetail': {'option': k, 'message': six.text_type(e)}}, status=400)

        options.set('sentry:version-configured', sentry.get_version())
        return Response(status=200)