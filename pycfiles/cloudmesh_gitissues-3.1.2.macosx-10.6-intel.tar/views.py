# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/big/ENV2/lib/python2.7/site-packages/cloudmesh_gitissues/views.py
# Compiled at: 2016-03-15 17:34:01
from __future__ import unicode_literals
from pprint import pprint
from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaulttags import register
from sqlalchemy.orm import sessionmaker
from django_jinja import library
from settings import REPOSITORIES

def Session():
    from aldjemy.core import get_engine
    engine = get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()


session = Session()

@library.global_function
def icon(name, color=None):
    if color is None:
        start = b''
        stop = b''
    else:
        start = (b'<font color="{}">').format(color)
        stop = b'</font>'
    if name in ('trash', ):
        icon_html = b'<i class="fa fa-trash-o"></i>'
    elif name in ('cog', ):
        icon_html = b'<i class="fa fa-cog"></i>'
    elif name in ('cog', ):
        icon_html = b'<i class="fa fa-info"></i>'
    elif name in ('off', ):
        icon_html = b'<i class="fa fa-power-off"></i>'
    elif name in ('on', ):
        icon_html = b'<i class="fa fa-power-off"></i>'
    elif name in ('refresh', ):
        icon_html = b'<i class="fa fa-refresh"></i>'
    elif name in ('chart', ):
        icon_html = b'<i class="fa fa-bar-chart"></i>'
    elif name in ('desktop', 'terminal'):
        icon_html = b'<i class="fa fa-desktop"></i>'
    elif name in ('info', ):
        icon_html = b'<i class="fa fa-info-circle"></i>'
    elif name in ('launch', ):
        icon_html = b'<i class="fa fa-rocket"></i>'
    else:
        icon_html = b'<i class="fa fa-question-circle"></i>'
    return start + icon_html + stop


@library.global_function
def state_color(state):
    if state.lower() in ('r', 'up', 'active', 'yes', 'true'):
        return (b'<span class="label label-success"> {} </span>').format(state)
    else:
        if state.lower() in ('down', 'down*', 'fail', 'false'):
            return (b'<span class="label label-danger"> {} </span>').format(state)
        if b'error' in str(state):
            return (b'<span class="label label-danger"> {} </span>').format(state)
        return (b'<span class="label label-default"> {} </span>').format(state)


def message(msg):
    return HttpResponse(b'Message: %s.' % msg)


def cloudmesh_vclusters(request):
    return message(b'Not yet Implemented')


@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key)
    if value is None:
        value = b'-'
    return value


def dict_table(request, **kwargs):
    context = kwargs
    return render(request, b'cloudmesh_gitissues/dict_table.jinja', context)


def list_table(request, **kwargs):
    context = kwargs
    return render(request, b'cloudmesh_gitissues/list_table.jinja', context)


def list_table_plain(request, **kwargs):
    context = kwargs
    return render(request, b'cloudmesh_gitissues/list_table_plain.jinja', context)


def list_table_html5(request, **kwargs):
    context = kwargs
    return render(request, b'cloudmesh_gitissues/list_table_html5.jinja', context)


def homepage(request):
    context = {b'title': b'Github Issues', 
       b'repos': REPOSITORIES}
    return render(request, b'cloudmesh_gitissues/home.jinja', context)