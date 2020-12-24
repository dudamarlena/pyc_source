# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Django\development\nimble\views\story_list.py
# Compiled at: 2017-01-30 10:02:51
# Size of source mod 2**32: 339 bytes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from nimble.models.story import Story

class StoryList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Story
    queryset = Story.objects.order_by('id')