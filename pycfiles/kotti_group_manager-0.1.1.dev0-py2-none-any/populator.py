# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/kotti_group_manager/kotti_group_manager/populator.py
# Compiled at: 2018-09-19 02:49:52
"""
Populate contains two functions that are called on application startup
(if you haven't modified kotti.populators).
"""
from kotti_controlpanel.util import add_settings
from kotti_group_manager.controlpanel import GroupRulesControlPanel

def populate():
    add_settings(GroupRulesControlPanel)