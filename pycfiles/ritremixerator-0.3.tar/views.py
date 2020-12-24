# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eitan/Documents/code/RITRemixerator/dorrie/../dorrie/comps/views.py
# Compiled at: 2012-02-01 17:51:56
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import NameForm, BasicForm
from helper import new_spin, add_lang_tz, select_helper, get_spin, handle_uploaded_ks
from parse import get_lang_tz, get_comps, default_selected, package_listing, build_ks, livecd_create, get_tail
import os

def home(request):
    """
    Get the name, base spin, and time defaults
    """
    defaults = {'name_of_the_spin': 'RIT_Remix', 'based_on': 'fedora-live-desktop.ks', 
       'select_timezone': 'America/New_York'}
    form = NameForm(initial=defaults)
    return render_to_response('home.html', {'form': form})


def packages(request):
    """
    Select packages and groups
    """
    if request.FILES:
        handle_uploaded_ks(request.FILES['uploaded_kickstart'])
    name = request.POST.get('name_of_the_spin')
    base_ks = request.POST.get('based_on')
    if name == None or base_ks == None:
        return HttpResponseRedirect('/')
    else:
        uploaded = False
        if base_ks == 'None':
            base_ks = os.path.join(settings.MEDIA_ROOT, request.FILES['uploaded_kickstart']._name)
            uploaded = True
        spin = new_spin(name, base_ks, uploaded)
        spin_id = spin.id
        language = request.POST.get('select_language')
        timezone = request.POST.get('select_timezone')
        if language == None or timezone == None:
            return HttpResponseRedirect('/')
        print spin.uploaded
        spin = add_lang_tz(spin_id, language, timezone)
        print spin.uploaded
        selected, plus, minus = default_selected(spin.baseks, spin.uploaded)
        c = get_comps()
        groups = package_listing(c)
        categories = c.get_categories()
        return render_to_response('packages.html', {'cats': categories, 'groups': groups, 
           'defaults': selected, 'spin': spin, 'plus': plus, 
           'minus': minus})


def select(request):
    """
    Record to backend when a select box is selected/unselected
    """
    spin_id = request.POST.get('spin_id')
    type = request.POST.get('type')
    action = request.POST.get('action')
    string = request.POST.get('string')
    html = select_helper(spin_id, type, action, string)
    return HttpResponse(html)


def build(request):
    """
    Build KS and later Image
    """
    spin_id = request.POST.get('spin_id')
    if spin_id == None:
        return HttpResponseRedirect('/')
    else:
        new_ks = build_ks(spin_id)
        spin = get_spin(spin_id)
        return render_to_response('build.html', {'ks': new_ks, 'spin': spin})


def process(request):
    """
    start livecd-creator as a separate process
    """
    spin_id = request.POST.get('spin_id')
    pid = livecd_create(spin_id)
    html = 'Process %s started..' % pid
    return HttpResponse(html)


def tail(request):
    """
    Return tail of the log
    """
    spin_id = request.POST.get('spin_id')
    html = get_tail(spin_id)
    return HttpResponse(html)