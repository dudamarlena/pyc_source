# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/section/context_processors.py
# Compiled at: 2011-08-24 05:30:52
from django.conf import settings
from django.core.urlresolvers import Resolver404
from snippetscream import resolve_to_name

def section(request):
    """
    Determines the current site section from resolved view pattern and adds
    it to context['section']. Section defaults to the first specified section.
    """
    try:
        sections = settings.SECTIONS
    except AttributeError:
        return {}
    else:
        section = sections[0]['name']
        try:
            pattern_name = resolve_to_name(request.path_info)
        except Resolver404:
            pattern_name = None

        if pattern_name:
            for option in settings.SECTIONS:
                if pattern_name in option['matching_pattern_names']:
                    section = option['name']

    return {'section': section}