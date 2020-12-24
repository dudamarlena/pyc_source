# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nfox/www/assets/assettools/duashttp/views/api.py
# Compiled at: 2014-10-30 10:23:41
# Size of source mod 2**32: 1703 bytes
from duashttp.serializers import AssetVersionSerializer
from duashttp.models import AssetVersion
from duashttp.filters import AssetVersionFilter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from django.http import HttpResponse
__all__ = [
 'AssetVersionViewSetBase']

class AssetVersionViewSetBase(viewsets.ModelViewSet):
    __doc__ = '\n    AssetVersionViewSetBase api control viewset\n    '
    queryset = AssetVersion.objects.all()
    serializer_class = AssetVersionSerializer
    permission_classes = [IsAuthenticated]
    filter_class = AssetVersionFilter

    @action(methods=['GET'])
    def blob(self, request, pk=None):
        """
        fetch large object from pg and gives it back to user via HTTP 1.1
        request

        :param request: django request instance
        :param pk: requested resource primary key
        :rtype: django.http.HttpResponse
        :rtype: HttpResponse
        :return: file with its filename stored in database
        """
        obj = self.get_object_or_none()
        if obj:
            blob = obj.get_blob_data()
            content_type = 'octet/stream'
            response = HttpResponse(blob, content_type=content_type, status=status.HTTP_200_OK)
            response['Content-Disposition'] = 'attachment; filename="%s"' % obj.name
            return response
        return HttpResponse('404', status=status.HTTP_404_NOT_FOUND, content_type='application/json')