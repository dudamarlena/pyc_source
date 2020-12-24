# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/schema.py
# Compiled at: 2008-09-11 19:48:09
__doc__ = 'Archetypes schema definitions for ruleset module, and other common\nschemas.'
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