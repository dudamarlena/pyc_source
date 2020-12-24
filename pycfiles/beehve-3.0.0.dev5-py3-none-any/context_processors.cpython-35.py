# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/devel/cfm/beehve/beehve/apps/honey/context_processors.py
# Compiled at: 2016-08-07 13:07:33
# Size of source mod 2**32: 577 bytes
from django.template import RequestContext
from .models import Project, Technology, Topic, Event
from workers.models import Worker
from django.contrib.auth import get_user_model

def menu_preloader(request):
    workers = Worker.objects.filter(active=True)
    projects = Project.objects.all()
    technologies = Technology.objects.all()
    topics = Topic.objects.all()
    events = Event.objects.all()
    return {'projects': projects, 
     'technologies': technologies, 
     'topics': topics, 
     'events': events, 
     'workers': workers}