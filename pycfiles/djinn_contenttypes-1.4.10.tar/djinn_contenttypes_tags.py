# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/templatetags/djinn_contenttypes_tags.py
# Compiled at: 2015-06-01 16:11:46
from django.template import Library
from django.utils.translation import ugettext as _
from django.conf import settings
from django.utils import dateformat
from djinn_workflow.utils import get_state
register = Library()

@register.simple_tag
def scheduled_line(obj):
    """ Return the object's 'scheduled' publishing """
    line = ''
    if obj.publish_from and obj.publish_to:
        line = _('From %(publish_from)s till %(publish_to)s') % {'publish_from': dateformat.format(obj.publish_from, settings.DATETIME_FORMAT), 
           'publish_to': dateformat.format(obj.publish_to, settings.DATETIME_FORMAT)}
    elif obj.publish_from:
        line = _('From %(publish_from)s') % {'publish_from': dateformat.format(obj.publish_from, settings.DATETIME_FORMAT)}
    elif obj.publish_to:
        line = _('Till %(publish_to)s') % {'publish_to': dateformat.format(obj.publish_to, settings.DATETIME_FORMAT)}
    return line


@register.simple_tag
def pub_classes(obj):
    """ publishing related CSS classes """
    classes = []
    if not hasattr(obj, 'is_published'):
        return ''
    if not obj.is_published:
        classes.append('unpublished')
    else:
        classes.append('published')
    if hasattr(obj, 'is_scheduled') and obj.is_scheduled:
        classes.append('scheduled')
    try:
        classes.append(get_state(obj).name)
    except:
        pass

    return (' ').join(classes)