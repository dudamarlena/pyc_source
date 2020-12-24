# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_killbill/serializers.py
# Compiled at: 2016-09-25 09:47:37
from rest_framework import serializers
from nodeconductor.core import serializers as core_serializers
from .models import Invoice

class InvoiceSerializer(core_serializers.AugmentedSerializerMixin, serializers.HyperlinkedModelSerializer):
    year = serializers.DateField(format='%Y', source='date')
    month = serializers.DateField(format='%m', source='date')
    customer_native_name = serializers.ReadOnlyField(source='customer.native_name')
    pdf = serializers.HyperlinkedIdentityField(view_name='invoice-pdf', lookup_field='uuid')
    usage_pdf = serializers.HyperlinkedIdentityField(view_name='invoice-usage-pdf', lookup_field='uuid')

    class Meta(object):
        model = Invoice
        fields = ('url', 'uuid', 'year', 'month', 'amount', 'pdf', 'usage_pdf', 'date',
                  'customer', 'customer_uuid', 'customer_name', 'customer_native_name')
        related_paths = ('customer', )
        extra_kwargs = {'url': {'lookup_field': 'uuid'}, 'customer': {'lookup_field': 'uuid'}}