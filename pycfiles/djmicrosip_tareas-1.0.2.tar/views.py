# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_tareas\djmicrosip_tareas\views.py
# Compiled at: 2020-01-17 20:06:16
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ProgrammedTaskForm
from .models import ProgrammedTask

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_tareas/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def tareas(request, template_name='djmicrosip_tareas/tareas.html'):
    tasks = ProgrammedTask.objects.all()
    context = {'tareas': tasks}
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def tarea(request, id=None, template_name='djmicrosip_tareas/tarea.html'):
    if id:
        task = get_object_or_404(ProgrammedTask, pk=id)
    else:
        task = ProgrammedTask()
    form = ProgrammedTaskForm(request.POST or None, instance=task)
    if form.is_valid():
        task = form.save(commit=False)
        task.save()
        return HttpResponseRedirect('/tareas/tareas/')
    else:
        context = {'form': form}
        return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def tarea_delete(request, id=None):
    if id:
        task = get_object_or_404(ProgrammedTask, pk=id)
        task.delete()
        return HttpResponseRedirect('/tareas/tareas/')