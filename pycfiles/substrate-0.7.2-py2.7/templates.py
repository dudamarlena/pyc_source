# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/lib/substrate/agar/django/templates.py
# Compiled at: 2012-02-03 19:38:43
"""
The ``agar.django.templates`` module contains function(s) to render django templates 
in a manner that is aware of template loaders and dirs configured in the DJANGO_SETTINGS_MODULE
"""

def render_template_to_string(template_path, context={}):
    """
    A helper function that renders a Django template as a string in a
    manner that is aware of the loaders and dirs configured in the
    DJANGO_SETTINGS_MODULE.

    :param template_path: the template path relative to a configured module directory

    :param context: a dictionary of context attributes to referenced within the template
    """
    from django.template import loader
    return loader.render_to_string(template_path, context)


def render_template(response, template_path, context=None):
    """
    A helper function that renders django templates in a manner that is aware of the loaders 
    and dirs configured in the DJANGO_SETTINGS_MODULE

    :param template_path: the template path relative to a configured module directory

    :param context: a dictionary of context attributes to referenced within the template
    """
    if context is None:
        context = {}
    from django.template import loader
    response.out.write(loader.render_to_string(template_path, context))
    return