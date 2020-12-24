# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tesla/template.py
# Compiled at: 2007-08-21 13:09:57
from paste.script import templates

class TeslaTemplate(templates.Template):
    egg_plugins = [
     'Tesla', 'Elixir']
    required_templates = ['pylons']
    _template_dir = 'templates/default'
    summary = 'Pylons+Elixir template'


class TeslaAuthTemplate(templates.Template):
    required_templates = [
     'tesla']
    _template_dir = 'templates/auth'
    summary = 'Tesla + authentication'


class TeslaAuthXpTemplate(templates.Template):
    required_templates = [
     'tesla_auth']
    _template_dir = 'templates/auth_xp'
    summary = 'Tesla + row-level authentication (experimental)'