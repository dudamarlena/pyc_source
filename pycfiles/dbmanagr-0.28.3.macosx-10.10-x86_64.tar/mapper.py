# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/dto/mapper.py
# Compiled at: 2015-10-11 07:17:06
import logging
from dbmanagr.dto.row import Row
from dbmanagr.dto.column import Column
from dbmanagr.dto.foreignkey import ForeignKey
from dbmanagr.dto.table import Table
from dbmanagr.dto.node import ColumnNode, ForeignKeyNode, TableNode, NameNode
logger = logging.getLogger(__name__)

def to_dto(model):
    if type(model) is dict:
        return dict(map(lambda (k, v): (k, to_dto(v)), model.iteritems()))
    if type(model) in (tuple, list, set):
        return map(to_dto, model)
    if model.__class__.__name__ == 'Row':
        return Row(table=to_dto(model.table), row=to_dto(model.row), autocomplete=model.autocomplete())
    if model.__class__.__name__ == 'Column':
        return Column(name=model.name, tablename=model.table.name, type_=model.type, nullable=model.nullable, default=model.default, autoincrement=model.autoincrement, primary_key=model.primary_key, autocomplete=model.autocomplete())
    if model.__class__.__name__ == 'ForeignKey':
        return ForeignKey(a=to_dto(model.a), b=to_dto(model.b))
    if model.__class__.__name__ == 'Table':
        return Table(name=model.name, uri=model.uri, owner=model.owner, size=model.size, primary_key=model.primary_key, columns=to_dto(model.columns()), foreign_keys=to_dto(model.foreign_keys()), autocomplete=model.autocomplete())
    if model.__class__.__name__ == 'ColumnNode':
        return ColumnNode(to_dto(model.column), model.indent)
    if model.__class__.__name__ == 'ForeignKeyNode':
        return ForeignKeyNode(to_dto(model.fk), to_dto(model.parent), model.indent)
    if model.__class__.__name__ == 'TableNode':
        return TableNode(to_dto(model.table), model.indent)
    if model.__class__.__name__ == 'NameNode':
        return NameNode(to_dto(model.name), model.indent)
    return model