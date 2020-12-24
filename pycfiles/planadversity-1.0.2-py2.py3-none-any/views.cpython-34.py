# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/planadversity/planadversity/apps/meditations/views.py
# Compiled at: 2014-12-30 21:23:17
# Size of source mod 2**32: 6069 bytes
import json
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView, ListView, View, TemplateView
from django.core import serializers
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from .models import Meditation, Response
from .forms import ResponseForm
from braces import views

class JsonView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, views.JSONResponseMixin, View):
    pass


class MeditationDetailView(JsonView, DetailView):
    model = Meditation


class MeditationListJSONView(JsonView, ListView):
    model = Meditation
    json_dumps_kwargs = {'indent': 2}

    def get(self, request, *args, **kwargs):
        context = serializers.serialize('json', self.get_queryset().all())
        return self.render_json_response(context)


class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomepageView, self).get_context_data(*args, **kwargs)
        meditation = None
        responded = None
        try:
            meditation = Meditation.objects.get(date=datetime.now().date())
        except:
            pass

        try:
            responded = Response.objects.filter(meditation=meditation, user=self.request.user.id)[0]
        except IndexError:
            pass

        context['todays_meditation'] = meditation
        context['responded'] = responded
        return context


class MeditationListView(JsonView, ListView):
    model = Meditation
    form_class = ResponseForm

    def get_context_data(self, *args, **kwargs):
        context = super(MeditationListView, self).get_context_data(*args, **kwargs)
        meditation = None
        responses = None
        try:
            meditation = Meditation.objects.get(date=datetime.now().date())
            responded = Response.objects.filter(meditation=meditation, user=self.request.user.id)
        except:
            pass

        context['responses'] = Response.objects.filter(user=self.request.user.id)
        context['meditation'] = meditation
        context['responded'] = responded
        return context


class ResponseDetailView(JsonView, views.LoginRequiredMixin, DetailView):
    model = Response

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return Response.objects.filter(user=self.request.user.id)
        return Response.objects.all()


class ResponseListView(JsonView, views.LoginRequiredMixin, ListView):
    model = Response

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return Response.objects.filter(user=self.request.user.id)
        return Response.objects.all()


class ResponseCreateView(JsonView, views.LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm

    def get_context_data(self, *args, **kwargs):
        context = super(ResponseCreateView, self).get_context_data(*args, **kwargs)
        meditation = None
        try:
            meditation = Meditation.objects.get(slug=self.request.GET.get('meditation'))
        except:
            pass

        context['meditation'] = meditation
        return context

    def get_success_url(self):
        return reverse('homepage', args=()) + '#about'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return super(ResponseCreateView, self).form_valid(form)