# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_migration/kotti_migration/views/view.py
# Compiled at: 2017-05-22 09:17:50
"""
Created on 2017-05-22
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from pyramid.view import view_config
from pyramid.view import view_defaults
from kotti_migration import _
from kotti_migration.fanstatic import css_and_js
from kotti_migration.views import BaseView