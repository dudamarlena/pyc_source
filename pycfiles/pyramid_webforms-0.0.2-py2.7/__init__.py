# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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