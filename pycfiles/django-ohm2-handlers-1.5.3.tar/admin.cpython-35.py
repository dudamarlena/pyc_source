# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/socialstatistics/admin.py
# Compiled at: 2016-12-07 10:08:27
# Size of source mod 2**32: 644 bytes
from django.contrib import admin
from . import models as socialstatistics_models

class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(socialstatistics_models.Twitter, AuthorAdmin)
admin.site.register(socialstatistics_models.TwitterSnapshot, AuthorAdmin)
admin.site.register(socialstatistics_models.LastTwitterSnapshot, AuthorAdmin)
admin.site.register(socialstatistics_models.Facebook, AuthorAdmin)
admin.site.register(socialstatistics_models.FacebookPage, AuthorAdmin)
admin.site.register(socialstatistics_models.FacebookPageSnapshot, AuthorAdmin)
admin.site.register(socialstatistics_models.LastFacebookPageSnapshot, AuthorAdmin)