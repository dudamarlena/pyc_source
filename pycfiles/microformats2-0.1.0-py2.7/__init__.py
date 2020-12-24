# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/microformats2/__init__.py
# Compiled at: 2018-03-17 16:30:06
import jsonschema
from .schema import Microformat, MicroformatsDocument
from .discovery import get_post_type, PostTypes
__all__ = [
 'validate', 'schema_for', 'get_post_type', 'PostTypes']

def schema_for(type):
    return Microformat.schema_for(type)


def validate(mf2):
    if 'type' in mf2:
        type = mf2.get('type', ['h-entry'])[0]
        schema = schema_for(type)
    else:
        schema = MicroformatsDocument.get_schema()
    jsonschema.validate(mf2, schema)