# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /code/s3direct/widgets.py
# Compiled at: 2019-07-27 06:30:08
from __future__ import unicode_literals
import os
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlunquote_plus
from django.conf import settings

class S3DirectWidget(widgets.TextInput):

    class Media:
        js = ('s3direct/dist/index.js', )
        css = {b'all': ('s3direct/dist/index.css', )}

    def __init__(self, *args, **kwargs):
        self.dest = kwargs.pop(b'dest', None)
        super(S3DirectWidget, self).__init__(*args, **kwargs)
        return

    def render(self, name, value, **kwargs):
        file_url = value or b''
        csrf_cookie_name = getattr(settings, b'CSRF_COOKIE_NAME', b'csrftoken')
        ctx = {b'policy_url': reverse(b's3direct'), 
           b'signing_url': reverse(b's3direct-signing'), 
           b'dest': self.dest, 
           b'name': name, 
           b'csrf_cookie_name': csrf_cookie_name, 
           b'file_url': file_url, 
           b'file_name': os.path.basename(urlunquote_plus(file_url))}
        return mark_safe(render_to_string(os.path.join(b's3direct', b's3direct-widget.tpl'), ctx))