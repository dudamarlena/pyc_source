# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rosborn/Documents/Computing/Repositories/nexpy/src/nexpy/examples/plugins/chopper/__init__.py
# Compiled at: 2016-05-11 10:41:57
from __future__ import absolute_import
from . import get_ei, convert_qe

def plugin_menu():
    menu = 'Chopper'
    actions = []
    actions.append(('Get Incident Energy', get_ei.show_dialog))
    actions.append(('Convert to Q-E', convert_qe.show_dialog))
    return (menu, actions)