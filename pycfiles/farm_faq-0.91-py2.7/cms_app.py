# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/faq/cms_app.py
# Compiled at: 2014-03-27 06:14:42
from django.utils.translation import ugettext_lazy as _
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class FaqHook(CMSApp):
    name = _('FAQs')
    urls = ['faq.urls']


apphook_pool.register(FaqHook)