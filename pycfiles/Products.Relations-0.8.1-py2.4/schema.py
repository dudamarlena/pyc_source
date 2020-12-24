# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/schema.py
# Compiled at: 2008-09-11 19:48:09
"""Archetypes schema definitions for ruleset module, and other common
schemas."""
from Products.Archetypes.public import *
BaseSchemaWithInvisibleId = BaseSchema.copy()
BaseSchemaWithInvisibleId['id'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}

def RulesetSchema():
    schema = BaseSchema.copy()
    id_widget_attrs = {'description': 'Relationship attribute for references created through this ruleset.', 'description_msgid': None, 'label': 'Identification'}
    schema['id'].widget.__dict__.update(id_widget_attrs)
    schema['id'].required = 1
    cf = TextField('about', default_content_type='text/restructured', default_output_type='text/html', allowable_content_types=('text/structured',
                                                                                                                                'text/restructured',
                                                                                                                                'text/plain-pre'), widget=TextAreaWidget(rows=8))
    schema.addField(cf)
    return schema


RulesetSchema = RulesetSchema()