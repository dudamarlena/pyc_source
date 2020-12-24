# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mjg/git/django/psu/psu-infotext/psu_infotext/views.py
# Compiled at: 2019-09-05 20:21:37
# Size of source mod 2**32: 1209 bytes
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from psu_infotext.models import Infotext
from psu_base.classes.Log import Log
from psu_base.services import utility_service
from psu_base.decorators import require_authority
log = Log()

@require_authority(['administrator', 'developer'])
def index(request):
    """
    Search page for locating infotext to be edited
    """
    log.trace()
    text_instances = Infotext.objects.filter(app_code=(utility_service.get_app_code()))
    log.end('infotext/index')
    return render(request, 'index.html', {'text_instances': text_instances})


@require_authority(['administrator', 'developer'])
def update(request):
    """
    Update a given infotext instance
    """
    log.trace()
    postdata = request.POST
    log.debug(f"POST data: {postdata}")
    text_instance = Infotext.objects.get(pk=(request.POST['id']))
    if text_instance:
        text_instance.set_content(request.POST['content'])
    content = text_instance.content
    log.end(f"infotext/update: {content}")
    return HttpResponse(text_instance.content)