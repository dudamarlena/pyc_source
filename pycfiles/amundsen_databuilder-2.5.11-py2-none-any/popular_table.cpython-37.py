# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/amundsen_common/models/popular_table.py
# Compiled at: 2020-02-13 16:36:56
# Size of source mod 2**32: 434 bytes
from typing import Optional
import attr
from marshmallow_annotations.ext.attrs import AttrsSchema

@attr.s(auto_attribs=True, kw_only=True)
class PopularTable:
    database = attr.ib()
    database: str
    cluster = attr.ib()
    cluster: str
    schema = attr.ib()
    schema: str
    name = attr.ib()
    name: str
    description = None
    description: Optional[str]


class PopularTableSchema(AttrsSchema):

    class Meta:
        target = PopularTable
        register_as_scheme = True