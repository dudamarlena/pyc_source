# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/urls.py
# Compiled at: 2014-08-09 03:47:51
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from plugshop import settings
from plugshop.views import *
from plugshop.exceptions import NoUrlFound
PREFIX = settings.URL_PREFIX
urlpatterns = patterns('plugshop.views', url('^$', ProductListView.as_view(), name='plugshop'), url('^products/$', ProductListView.as_view(), name='plugshop-product-list'), url('^categories/$', CategoryListView.as_view(), name='plugshop-caterory-list'), url('^products/(?P<category_path>[\\-\\/\\w]+)/$', CategoryView.as_view(), name='plugshop-category'), url('^products/(?P<category_path>[\\-\\/\\w]+)/(?P<slug>[\\-\\/\\w]+)$', ProductView.as_view(), name='plugshop-product'), url('^cart/$', CartView.as_view(), name='plugshop-cart'), url('^order/(?P<number>[\\-\\/\\w]+)$', OrderView.as_view(), name='plugshop-order'), url('^order/$', OrderCreateView.as_view(), name='plugshop-order-new'))

def get_url(name):
    patterns = filter(lambda x: x.name == name, urlpatterns)
    try:
        pattern = patterns[0]
    except IndexError:
        raise NoUrlFound(_("No url with name '%s'") % name)

    return pattern._regex