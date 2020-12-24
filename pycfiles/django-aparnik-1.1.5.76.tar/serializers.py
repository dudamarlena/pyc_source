# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/api/serializers.py
# Compiled at: 2018-12-03 11:15:34
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from aparnik.contrib.basemodels.api.serializers import BaseModelListSerializer, BaseModelDetailSerializer, ModelListPolymorphicSerializer
from ..models import Voucher

class VoucherListSerializer(BaseModelListSerializer):

    def __init__(self, *args, **kwargs):
        super(VoucherListSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Voucher
        fields = BaseModelListSerializer.Meta.fields + [
         'quantity',
         'expire_at',
         'is_active',
         'is_spent',
         'price',
         'price_string']


class VoucherDetailsSerializers(VoucherListSerializer, BaseModelDetailSerializer):

    def __init__(self, *args, **kwargs):
        super(VoucherDetailsSerializers, self).__init__(*args, **kwargs)

    class Meta:
        model = Voucher
        fields = VoucherListSerializer.Meta.fields + BaseModelDetailSerializer.Meta.fields + []