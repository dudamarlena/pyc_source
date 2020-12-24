# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/wiki/templatetags/wikimenu.py
# Compiled at: 2009-01-08 09:11:51
from django import template
from softwarefabrica.django.wiki.models import *
from softwarefabrica.django.utils.viewshelpers import static_media_images_prefix
register = template.Library()

@register.inclusion_tag('wiki/tags/wikimenu.html')
def wikimenu(current=None, parent=None, level=0, maxrec=5, maxnum=30):
    wikis = Wiki.objects.filter(parent=parent).order_by('-created')[:maxnum]
    if level >= maxrec:
        return {}
    images = static_media_images_prefix()
    return {'level': level, 'nextlevel': level + 1, 'maxrec': maxrec, 'current': current, 'wikis': wikis, 'images': static_media_images_prefix(), 'folderopen': images + '/folderopen.gif', 'folder': images + '/folder.gif'}