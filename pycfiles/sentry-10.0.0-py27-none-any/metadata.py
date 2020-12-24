# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/cloudflare/metadata.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import logging, six
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sentry.api.base import Endpoint
logger = logging.getLogger('sentry.integrations.cloudflare')

class CloudflareMetadataEndpoint(Endpoint):
    permission_classes = (
     IsAuthenticated,)

    def get(self, request):
        logger.info('cloudflare.metadata', extra={'user_id': request.user.id})
        return Response({'metadata': {'username': request.user.username, 
                        'userId': six.text_type(request.user.id), 
                        'email': request.user.email}})