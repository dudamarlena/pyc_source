# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/templatetags/video_filters.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 706 bytes
from django.template import Library
register = Library()

@register.filter
def assign_mapped_fields(obj):
    """assign mapped field from custom registration form to registrant"""
    if hasattr(obj, 'custom_reg_form_entry'):
        if obj.custom_reg_form_entry:
            obj.assign_mapped_fields()
    return obj


@register.filter
def video_embed(video, width):
    """
    Return a video at the specified width
    """
    from django.template.defaultfilters import safe
    from tendenci.apps.videos.utils import ASPECT_RATIO
    try:
        width = int(width)
    except ValueError:
        width = 600

    height = int(round(width / ASPECT_RATIO))
    return safe(video.embed_code(width=width, height=height))