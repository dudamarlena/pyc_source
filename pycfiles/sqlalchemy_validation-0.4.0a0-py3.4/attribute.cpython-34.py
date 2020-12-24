# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlalchemy_validation/attribute.py
# Compiled at: 2015-12-30 19:34:46
# Size of source mod 2**32: 530 bytes
"""
"""
import sqlalchemy as sa

def set_attribute(column):
    """
    """

    def wrap(model, value, oldvalue, initiator):
        column.validator.validate(model, value)

    return wrap


def validate_attribute(Model):
    """
    """
    table = Model.__table__
    columns = table.columns
    constraints = table.constraints
    primary_key = table.primary_key
    for column_name, column in columns.items():
        attribute = getattr(Model, column_name)
        sa.event.listen(attribute, 'set', set_attribute(column))