# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/review_together/admin_urls.py
# Compiled at: 2015-02-02 13:34:36
from django.conf.urls import patterns, url
from review_together.extension import ReviewTogether
from review_together.forms import ReviewTogetherSettingsForm
urlpatterns = patterns('', url('^$', 'reviewboard.extensions.views.configure_extension', {'ext_class': ReviewTogether, 
   'form_class': ReviewTogetherSettingsForm}))