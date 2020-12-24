# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/aghoo/Aghoo/province/api/views.py
# Compiled at: 2018-01-09 01:46:23
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from dal import autocomplete
from django.db.models import Q
from province.models import Province, City, Shahrak, Town
from province.api.serializers import ProvinceListSerializer, ProvinceCreateSerializer, ProvinceDetailSerializer, CityListSerializer, CityCreateSerializer, CityDetailSerializer, ShahrakCreateSerializer, ShahrakDetailSerializer, ShahrakListSerializer, TownCreateSerializer, TownDetailSerializer, TownListSerializer
permission_create = [
 IsAdminUser]
permission_read = [AllowAny]

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10


def get_province(kwargs):
    return kwargs.get('province_id', 0)


def get_city(kwargs):
    return kwargs.get('city_id', 0)


class ProvinceListAPIView(ListAPIView):
    serializer_class = ProvinceListSerializer
    permission_classes = permission_read
    queryset = Province.objects.all()
    pagination_class = LargeResultsSetPagination


class ProvinceCreateAPIView(CreateAPIView):
    serializer_class = ProvinceCreateSerializer
    permission_classes = permission_create


class ProvinceDetailAPIView(RetrieveAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceDetailSerializer
    permission_classes = permission_read
    lookup_field = 'id'


class CityListAPIView(ListAPIView):
    serializer_class = CityListSerializer
    permission_classes = permission_read
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        province = get_province(self.kwargs)
        return City.objects.filter(province=province)


class CityCreateAPIView(CreateAPIView):
    serializer_class = CityCreateSerializer
    permission_classes = permission_create


class CityDetailAPIView(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer
    permission_classes = permission_read
    lookup_field = 'id'


class CityAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return City.objects.none()
        qs = City.objects.all()
        if self.q:
            qs = qs.filter(Q(title__istartswith=self.q))
        return qs[:10]


class ShahrakListAPIView(ListAPIView):
    serializer_class = ShahrakListSerializer
    permission_classes = permission_read
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        province = get_province(self.kwargs)
        return Shahrak.objects.filter(province=province)


class ShahrakCreateAPIView(CreateAPIView):
    serializer_class = ShahrakCreateSerializer
    permission_classes = permission_create


class ShahrakDetailAPIView(RetrieveAPIView):
    queryset = Shahrak.objects.all()
    serializer_class = ShahrakDetailSerializer
    permission_classes = permission_read
    lookup_field = 'id'


class TownListAPIView(ListAPIView):
    serializer_class = TownListSerializer
    permission_classes = permission_read
    queryset = Town.objects.all()
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        city = get_city(self.kwargs)
        return Town.objects.filter(city=city)


class TownCreateAPIView(CreateAPIView):
    serializer_class = TownCreateSerializer
    permission_classes = permission_create


class TownDetailAPIView(RetrieveAPIView):
    queryset = Town.objects.all()
    serializer_class = TownDetailSerializer
    permission_classes = permission_read
    lookup_field = 'id'