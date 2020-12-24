# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/das-g/hsr/dev/osmaxx/drf-utm-zone-info/utm_zone_info/views.py
# Compiled at: 2017-01-12 05:41:10
# Size of source mod 2**32: 1073 bytes
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utm_zone_info.coordinate_reference_system import utm_zones_for_representing
from utm_zone_info.serializers import GeometrySerializer

class UTMZoneSRIDView(APIView):
    __doc__ = '\n    A simple View accepting a geometry and returning SRIDs of UTM Zones that can represent this geometry.\n    '
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = GeometrySerializer(data=request.data)
        if serializer.is_valid():
            geometry = serializer.validated_data['geom']
            geometry.srid = serializer.validated_data['srid']
            data = dict(utm_zone_srids=[zone.srid for zone in utm_zones_for_representing(geometry)])
            return Response(data=data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


utm_zone_info = UTMZoneSRIDView.as_view()