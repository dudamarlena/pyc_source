# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/voice/admin.py
# Compiled at: 2011-09-23 19:07:57
from django.contrib import admin
from voice.models import Feature, Vote

class FeatureAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )


class VoteAdmin(admin.ModelAdmin):
    readonly_fields = ('feature', 'used_facebook', 'used_twitter', 'voter')


admin.site.register(Vote, VoteAdmin)
admin.site.register(Feature, FeatureAdmin)