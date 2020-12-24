# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skins/loader.py
# Compiled at: 2010-03-19 19:00:41
"""Wrapper for loading skin templates from the filesystem.

:Authors:
    - Bruce Kroeze
"""
__docformat__ = 'restructuredtext'
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.utils._os import safe_join
from skin import active_skin
import logging
log = logging.getLogger('skins.loader')

def get_template_sources(template_name, template_dirs=None):
    if not template_dirs:
        skin = active_skin()
        template_dirs = (skin.path,)
    for template_dir in template_dirs:
        try:
            yield safe_join(template_dir, template_name)
        except ValueError:
            pass


def load_template_source(template_name, template_dirs=None):
    for filepath in get_template_sources(template_name, template_dirs):
        try:
            return (
             open(filepath).read().decode(settings.FILE_CHARSET), filepath)
        except IOError:
            pass

    raise TemplateDoesNotExist, template_name


load_template_source.is_usable = True