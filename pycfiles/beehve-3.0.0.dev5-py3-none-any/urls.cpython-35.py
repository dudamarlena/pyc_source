# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/devel/cfm/beehve/beehve/apps/workers/urls.py
# Compiled at: 2016-08-07 14:06:22
# Size of source mod 2**32: 1477 bytes
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.conf.urls import url
from .views import WorkerListJSONView, WorkerListView, WorkerDetailView, WorkerUpdateView, WorkerProfileView, PositionListView, PositionDetailView
from .models import Worker
urlpatterns = [
 url('^profile/edit/', view=WorkerUpdateView.as_view(), name='worker-update'),
 url('^profile/', view=WorkerProfileView.as_view(), name='profile-detail'),
 url('^workers.json', view=WorkerListJSONView.as_view(), name='worker-list-json'),
 url('^workers/(?P<slug>[-\\w]+)/', view=WorkerDetailView.as_view(), name='worker-detail'),
 url('^workers/', view=WorkerListView.as_view(), name='worker-list'),
 url('^positions/(?P<slug>[-\\w]+)/', view=PositionDetailView.as_view(), name='position-detail'),
 url('^positions/', view=PositionListView.as_view(), name='position-list')]

def get_or_create_worker(sender, instance, **kwargs):
    Worker.objects.get_or_create(user=instance)


post_save.connect(get_or_create_worker, sender=get_user_model(), dispatch_uid='get_or_create_worker')
get_user_model().worker = property(lambda u: Worker.objects.get_or_create(user=u)[0])