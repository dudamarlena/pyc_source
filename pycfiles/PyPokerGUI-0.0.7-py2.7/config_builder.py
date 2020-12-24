# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pypokergui/config_builder.py
# Compiled at: 2017-04-01 11:23:14
import yaml

def build_config(max_round=None, initial_stack=None, small_blind=None, ante=None, blind_structure=None):
    config = {'max_round': max_round, 
       'initial_stack': initial_stack, 
       'small_blind': small_blind, 
       'ante': ante, 
       'blind_structure': blind_structure, 
       'ai_players': [{'name': 'FIXME:your-ai-name', 'path': 'FIXME:your-setup-script-path'}]}
    print yaml.dump(config, default_flow_style=False)