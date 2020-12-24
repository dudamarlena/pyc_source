# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/views.py
# Compiled at: 2018-01-09 13:54:21
from jmbo.views import ObjectDetail, ObjectList
from banner.models import Banner

class BannerDetailView(ObjectDetail):
    model = Banner
    template_name = 'banner/banner_detail.html'


class BannerListView(ObjectList):
    model = Banner
    template_name = 'banner/banner_list.html'