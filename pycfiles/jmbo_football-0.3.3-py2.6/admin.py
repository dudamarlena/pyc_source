# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/football/admin.py
# Compiled at: 2012-12-03 05:37:28
from django.contrib import admin
from django import forms
from jmbo.admin import ModelBaseAdmin
from football.models import League, Team, Fixture, LogEntry, Trivia, Player, LeagueGroup

class TeamInline(admin.StackedInline):
    model = Team


class FixtureInline(admin.StackedInline):
    model = Fixture


class LogEntryInline(admin.StackedInline):
    model = LogEntry


class LeagueAdmin(ModelBaseAdmin):
    inlines = [
     FixtureInline, LogEntryInline]

    def get_formsets(self, request, obj=None):
        for inline in obj is not None and self.get_inline_instances(request) or []:
            yield inline.get_formset(request, obj)

        return

    def response_add(self, request, obj, post_url_continue='../%s/'):
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        return super(LeagueAdmin, self).response_add(request, obj, post_url_continue)


class LeagueGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'football365_ci', 'football365_di', 'position')
    list_editable = ('football365_ci', 'football365_di', 'position')


class TeamAdmin(ModelBaseAdmin):
    pass


class TriviaAdmin(ModelBaseAdmin):
    pass


class PlayerAdmin(ModelBaseAdmin):
    pass


admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueGroup, LeagueGroupAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Trivia, TriviaAdmin)
admin.site.register(Player, PlayerAdmin)