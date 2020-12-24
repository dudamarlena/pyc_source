# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/templates.py
# Compiled at: 2006-10-22 17:01:02
import os
from paste.script.templates import Template

class WebKit(Template):
    __module__ = __name__
    _template_dir = 'paster_templates/webkit'
    summary = 'A Paste WebKit web application'
    egg_plugins = [
     'PasteWebKit']
    required_templates = [
     'PasteDeploy#paste_deploy']