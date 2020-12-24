# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_jsondash/flask_jsondash/schema.py
# Compiled at: 2017-06-13 14:26:51
# Size of source mod 2**32: 5795 bytes
"""
flask_jsondash.schema
~~~~~~~~~~~~~~~~~~~~~

The core schema definition and validation rules.

:copyright: (c) 2016 by Chris Tabor.
:license: MIT, see LICENSE for more details.
"""
import cerberus
from .settings import CHARTS_CONFIG

def get_chart_types():
    """Get all available chart 'type' names from core config.

    Returns:
        types (list): A list of all possible chart types, under all families.
    """
    types = []
    charts = [chart['charts'] for chart in CHARTS_CONFIG.values()]
    for group in charts:
        for chart in group:
            types.append(chart[0])

    return types


CHART_INPUT_SCHEMA = {'btn_classes': {'type': 'list', 
                 'schema': {'type': 'string'}}, 
 
 'submit_text': {'type': 'string'}, 
 
 'options': {'type': 'list', 
             'schema': {'type': 'dict', 
                        'schema': {'options': {'type': 'list', 
                                               'schema': {'type': 'list', 
                                                          'minlength': 2, 
                                                          'maxlength': 2}}, 
                                   
                                   'type': {'type': 'string', 
                                            'allowed': [
                                                        'number', 'select', 'radio',
                                                        'checkbox', 'text',
                                                        'password',
                                                        'color',
                                                        'date',
                                                        'datetime-local',
                                                        'month',
                                                        'week',
                                                        'time',
                                                        'email',
                                                        'number',
                                                        'range',
                                                        'search',
                                                        'tel',
                                                        'url'], 
                                            
                                            'default': 'text'}, 
                                   
                                   'name': {'type': 'string', 
                                            'required': True}, 
                                   
                                   'default': {'anyof': [
                                                         {'type': 'string'},
                                                         {'type': 'number'},
                                                         {'type': 'boolean'}], 
                                               
                                               'nullable': True}, 
                                   
                                   'validator_regex': {'nullable': True, 
                                                       'type': 'string'}, 
                                   
                                   'placeholder': {'nullable': True, 
                                                   'anyof': [
                                                             {'type': 'string'},
                                                             {'type': 'number'}]}, 
                                   
                                   'label': {'type': 'string'}, 
                                   
                                   'input_classes': {'type': 'list', 
                                                     'schema': {'type': 'string'}}}}}}
CHART_SCHEMA = {'type': 'dict', 
 'schema': {'name': {'type': 'string', 
                     'required': True}, 
            
            'guid': {'type': 'string', 
                     'required': True, 
                     'regex': '[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+'}, 
            
            'order': {'type': 'number', 
                      'nullable': True, 
                      'default': 0}, 
            
            'row': {'type': 'number', 
                    'nullable': True, 
                    'default': 0}, 
            
            'refresh': {'type': 'boolean', 
                        'nullable': True}, 
            
            'refreshInterval': {'type': 'number', 
                                'nullable': True}, 
            
            'height': {'type': 'number', 
                       'required': True}, 
            
            'width': {'anyof': [
                                {'type': 'string'},
                                {'type': 'number'}], 
                      
                      'regex': '(col-[0-9]+)|([0-9]+)', 
                      'required': True}, 
            
            'dataSource': {'type': 'string', 
                           'required': True}, 
            
            'family': {'type': 'string', 
                       'required': True, 
                       'allowed': list(CHARTS_CONFIG.keys())}, 
            
            'type': {'type': 'string', 
                     'required': True, 
                     'allowed': get_chart_types()}, 
            
            'inputs': {'type': 'dict', 
                       'schema': CHART_INPUT_SCHEMA}}}
DASHBOARD_SCHEMA = {'name': {'type': 'string', 
          'required': True}, 
 
 'id': {'type': 'string', 
        'required': True, 
        'regex': '[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+'}, 
 
 'date': {'type': 'string', 
          'required': True}, 
 
 'layout': {'type': 'string', 
            'required': True, 
            'allowed': ['freeform', 'grid']}, 
 
 'modules': {'type': 'list', 
             'schema': CHART_SCHEMA, 
             'required': True}}

def validate(conf):
    """Validate a json conf."""
    v = cerberus.Validator(DASHBOARD_SCHEMA, allow_unknown=True)
    valid = v.validate(conf)
    if not valid:
        return v.errors