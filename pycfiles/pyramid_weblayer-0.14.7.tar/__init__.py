# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_webforms/__init__.py
# Compiled at: 2013-01-21 13:20:51
from .api import Form
from .api import CSRF_TOKEN_KEY
from .api import form_errors

def includeme(config):
    """Pyramid configuration entry point"""
    from .api import forms_renderer_factory
    config.add_renderer('.p_wf_mako', forms_renderer_factory)
    config.add_translation_dirs('pyramid_webforms:locale/')