# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scrumtools/base.py
# Compiled at: 2014-11-11 10:11:03
"""
Copyright 2010-2014 DIMA Research Group, TU Berlin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Created on Apr 13, 2014
"""
from __future__ import absolute_import
from cement.core import controller

class BaseController(controller.CementBaseController):

    class Meta:
        label = 'base'
        description = 'A set of batch management tools for GitHub and Trello.'
        config_section = 'core'
        config_defaults = dict(users_file=None, users_file_skip_first=False, users_file_delimiter=';', users_file_escape_char=None, users_schema='ID;Username;Group;Github;Trello', users_schema_key_id='ID', users_schema_key_username='Username', users_schema_key_group='Group', users_schema_key_github='Github', users_schema_key_trello='Trello')

    @controller.expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])