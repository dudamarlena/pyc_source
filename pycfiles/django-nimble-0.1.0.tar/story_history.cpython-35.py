# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Django\development\nimble\views\story_history.py
# Compiled at: 2017-01-30 17:02:42
# Size of source mod 2**32: 1257 bytes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views.generic import DetailView
from nimble.models.story import Story

class StoryHistory(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Story
    reverse_url = 'story_history'
    template_name = 'nimble/story_history.html'

    def get(self, *args, **kwargs):
        self.ident = kwargs.get('ident')
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story = self.get_object()
        if self.ident != story.ident:
            raise Http404('Object does not exist')
        revisions = story.revision_numbers()
        context['history'] = []
        context['active_tab'] = 'history'
        for index, value in enumerate(revisions, start=1):
            if index == len(revisions):
                break
            context['history'].append({'title': 'Change {}'.format(index), 
             'table': story.difference_tables_between_revisions(value, revisions[index])})

        return context