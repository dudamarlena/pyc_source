# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-pay2pay/pay2pay/urls.py
# Compiled at: 2013-07-01 02:43:41
from django.conf.urls import patterns, url
from .views import Confirm
from .views import PaymentFail
from .views import PaymentSuccess
urlpatterns = patterns('', url('^confirm/$', Confirm.as_view(), name='pay2pay_confirm'), url('^success/$', PaymentFail.as_view(), name='pay2pay_success'), url('^fail/$', PaymentSuccess.as_view(), name='pay2pay_fail'))