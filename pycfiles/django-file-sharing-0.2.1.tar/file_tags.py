# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vahid/workspace/nooir/file_sharing/templatetags/file_tags.py
# Compiled at: 2013-02-12 14:35:51
from django.template import Library
register = Library()

@register.filter
def get_icon(mime):
    if mime.startswith('image'):
        return 'icon-picture'
    if mime.startswith('text'):
        return 'icon-file'
    if mime.startswith('video'):
        return 'icon-film'
    if mime.startswith('audio'):
        return 'icon-music'