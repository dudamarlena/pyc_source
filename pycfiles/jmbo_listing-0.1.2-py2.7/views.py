# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/listing/views.py
# Compiled at: 2017-05-06 10:55:04
from django.views.generic.detail import DetailView
from listing.models import Listing

class ListingDetail(DetailView):
    model = Listing
    template_name = 'listing/listing_detail.html'

    def get_queryset(self):
        return Listing.permitted.all()