# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/publisher/admin.py
# Compiled at: 2011-10-05 09:27:43
from django.contrib import admin
from publisher.models import Buzz, Facebook, Mobile, SocialBookmark, Twitter, Web
admin.site.register(Buzz)
admin.site.register(Facebook)
admin.site.register(Mobile)
admin.site.register(SocialBookmark)
admin.site.register(Twitter)
admin.site.register(Web)