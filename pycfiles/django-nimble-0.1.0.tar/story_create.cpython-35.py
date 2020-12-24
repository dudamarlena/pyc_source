# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Django\development\nimble\views\story_create.py
# Compiled at: 2017-01-30 17:02:42
# Size of source mod 2**32: 2705 bytes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from nimble.forms.debt import DebtForm
from nimble.forms.feature import FeatureForm
from nimble.models.debt import Debt
from nimble.models.feature import Feature
from nimble.models.story import Story
form_mapping = {'debt': {'model': Debt, 
          'form': DebtForm}, 
 
 'feature': {'model': Feature, 
             'form': FeatureForm}}

def get_model(name):
    return form_mapping.get(name, {}).get('model')


def get_form(name):
    return form_mapping.get(name, {}).get('form')


class Display(CreateView):
    model = Story
    reverse_url = 'story_detail'
    template_name = 'nimble/story_create.html'

    def get_form_class(self, *args, **kwargs):
        return get_form(self.story_type)

    def get(self, *args, **kwargs):
        self.story_type = kwargs.get('story_type')
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_class = get_model(self.story_type)
        context['story_type'] = model_class.typename
        context['api_url'] = model_class.api_list_url()
        print(dir(context['form'].fields['description']))
        return context


class Post(SingleObjectMixin, FormView):
    template_name = 'nimble/story_create.html'
    model = Story
    reverse_url = 'story_detail'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.story_type = kwargs.get('story_type')
        self.form_class = get_form(self.story_type)
        model_class = get_model(self.story_type)
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = model_class.create(self.request.user, **form.cleaned_data)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(self.reverse_url, kwargs={'pk': self.object.pk, 'ident': self.object.ident})


class StoryCreate(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        view = Display.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = Post.as_view()
        return view(request, *args, **kwargs)