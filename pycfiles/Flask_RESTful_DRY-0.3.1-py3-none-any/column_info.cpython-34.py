# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/model/column_info.py
# Compiled at: 2015-04-13 12:00:21
# Size of source mod 2**32: 5017 bytes
"""The Column_info class.
"""
from itertools import groupby
import operator
from sqlalchemy.dialects.postgresql import ENUM
from flask import current_app
from .utils import db, lookup_model

class Column_info:
    sequence = None

    def __init__(self, model, col_name, col):
        self.model_name = model.__name__
        self.col_name = col_name
        if isinstance(col.type, (db.Enum, ENUM)):
            self.col_type = col.type.enums
        else:
            type_ = str(col.type).lower()
            if type_.startswith('varchar') or type_.startswith('string') or type_.startswith('text'):
                type_ = 'string'
            if type_ == 'smallint':
                type_ = 'integer'
            self.col_type = type_
        self.nullable = col.nullable
        self.has_default = col.server_default is not None
        self.optional = self.nullable or self.has_default
        if col.primary_key:
            if col.autoincrement:
                self.sequence = '{}_{}_seq'.format(model.__tablename__, col_name)
            model._dry_primary_keys.append(col_name)
            constraint_name = '{}_pkey'.format(model.__tablename__)
            if constraint_name in current_app.dry_unique_constraints:
                current_app.dry_unique_constraints[constraint_name] += (
                 col_name, 'Duplicate value.')
            else:
                current_app.dry_unique_constraints[constraint_name] = (
                 (
                  col_name, 'Duplicate value.'),)
        if col.unique:
            assert not col.primary_key
            constraint_name = '{}_{}_key'.format(model.__tablename__, col_name)
            current_app.dry_unique_constraints[constraint_name] = (
             (
              col_name, 'Duplicate value.'),)
        self.validators = col.dry_validators
        if col.foreign_keys:
            assert len(col.foreign_keys) == 1, 'name {}, len {}'.format(col_name, len(col.foreign_keys))
            foreign_key = col.foreign_keys.pop()
            col.foreign_keys.add(foreign_key)
            other_table, other_column = foreign_key.target_fullname.split('.')
            constraint_name = '{}_{}_fkey'.format(model.__tablename__, col_name)
            current_app.dry_foreign_key_constraints[constraint_name] = (
             col_name, 'Not found.')
            model._dry_links[col_name] = lookup_model(other_table)

    def validate(self, value, for_update):
        """Validates `value` against the validators for this column.

        Returns revised value, list of errors.
        """
        errors = []
        if value is None:
            if not self.nullable:
                if for_update:
                    errors.append('Value is not optional')
                elif not self.has_default:
                    errors.append('Required value')
        else:
            for v in self.validators:
                value, error = v(self.col_name, value)
                if error:
                    errors.append(error)
                    continue

        return (
         value, errors)

    def validator_info(self):
        """Yields validator_type, info for each validator on this column.

        `info` is (regex, message) or a list of these depending on the
        validator_type.
        """
        for val_type, specs in groupby(sorted(fn.info for fn in self.validators if fn.info is not None), key=operator.itemgetter(0)):
            if val_type in ('must_not_include_regex', 'must_not_match_regex'):
                yield (
                 val_type,
                 [(regex, message) for _, regex, message in specs])
            else:
                specs = tuple(specs)
                assert len(specs) == 1, '{}.{}: multiple {} validators not allowed'.format(self.model_name, self.col_name, val_type)
                _, regex, message = specs[0]
                yield (val_type, (regex, message))