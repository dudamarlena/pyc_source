# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cloudinary_storage/templatetags/cloudinary_static.py
# Compiled at: 2020-03-05 09:52:53
# Size of source mod 2**32: 737 bytes
from cloudinary import CloudinaryResource
from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag(name='cloudinary_static', takes_context=True)
def cloudinary_static(context, image, options_dict={}, **options):
    options = dict(options_dict, **options)
    try:
        if context['request'].is_secure():
            if 'secure' not in options:
                options['secure'] = True
    except KeyError:
        pass
    else:
        if not isinstance(image, CloudinaryResource):
            image = staticfiles_storage.stored_name(image)
            image = CloudinaryResource(image)
        return mark_safe((image.image)(**options))