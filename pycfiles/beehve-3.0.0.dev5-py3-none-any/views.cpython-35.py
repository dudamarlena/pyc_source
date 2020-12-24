# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/devel/cfm/beehve/beehve/apps/workers/views.py
# Compiled at: 2016-08-07 13:18:14
# Size of source mod 2**32: 1731 bytes
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView, ListView, View
from django.core import serializers
from django.core.urlresolvers import reverse
from .models import Worker, Position
from .forms import WorkerForm
from braces import views

class JsonView(views.CsrfExemptMixin, views.JsonRequestResponseMixin, views.JSONResponseMixin, View):
    pass


class WorkerListJSONView(JsonView, ListView):
    model = Worker
    json_dumps_kwargs = {'indent': 2}
    queryset = Worker.objects.filter(active=True)

    def get(self, request, *args, **kwargs):
        context = serializers.serialize('json', self.get_queryset().all())
        return self.render_json_response(context)


class WorkerDetailView(DetailView):
    model = Worker
    slug_field = 'user__username'
    queryset = Worker.objects.filter(active=True)


class WorkerListView(ListView):
    model = Worker
    queryset = Worker.objects.filter(active=True)


class PositionDetailView(DetailView):
    model = Position
    queryset = Position.objects.all()


class PositionListView(ListView):
    model = Position
    queryset = Position.objects.all()


class WorkerUpdateView(UpdateView):
    model = Worker
    form_class = WorkerForm
    queryset = Worker.objects.filter(active=True)

    def get_success_url(self):
        return reverse('profile-detail')

    def get_object(self, *args, **kwargs):
        return self.request.user.worker


class WorkerProfileView(DetailView):
    model = Worker
    queryset = Worker.objects.filter(active=True)

    def get_object(self, *args, **kwargs):
        return self.request.user