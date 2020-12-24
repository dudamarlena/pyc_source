# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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