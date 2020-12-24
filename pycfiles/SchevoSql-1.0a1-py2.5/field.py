# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevosql/field.py
# Compiled at: 2008-01-19 12:36:32
"""Schevo field SQL operations.

For copyright, license, and warranty, see bottom of file.
"""
from dispatch import generic
from schevo.constant import UNASSIGNED
from schevo import field as F
[
 generic()]

def to_colspec(dialect, field):
    """Return a tuple of (specs, constraints) for the field."""
    pass


[
 generic()]

def to_data(dialect, field):
    """Return a tuple of (col name, value) suitable for INSERT."""
    pass


[
 to_colspec.when("dialect == 'jet' and isinstance(field, F.Field)")]

def to_colspec(dialect, field):
    if field.max_size is not None:
        max_size = '(%i)' % field.max_size
    else:
        max_size = ''
    specs = [
     '`{table}_%s` TEXT %s %s' % (field._attribute,
      max_size,
      ('', ' NOT NULL')[field.required])]
    constraints = []
    return (
     specs, constraints)


[
 to_colspec.when("dialect == 'jet' and isinstance(field, F.Integer)")]

def to_colspec(dialect, field):
    specs = [
     '`{table}_%s` INTEGER %s' % (field._attribute,
      ('', ' NOT NULL')[field.required])]
    constraints = []
    return (
     specs, constraints)


[
 to_colspec.when("dialect == 'jet' and isinstance(field, F.Float)")]

def to_colspec(dialect, field):
    specs = [
     '`{table}_%s` FLOAT %s' % (field._attribute,
      ('', ' NOT NULL')[field.required])]
    constraints = []
    return (
     specs, constraints)


[
 to_colspec.when("dialect == 'jet' and isinstance(field, F.Money)")]

def to_colspec(dialect, field):
    specs = [
     '`{table}_%s` FLOAT %s' % (field._attribute,
      ('', ' NOT NULL')[field.required])]
    constraints = []
    return (
     specs, constraints)


[
 to_colspec.when("dialect == 'jet' and isinstance(field, F.Boolean)")]

def to_colspec(dialect, field):
    specs = [
     '`{table}_%s` BIT %s' % (field._attribute,
      ('', ' NOT NULL')[field.required])]
    constraints = []
    return (
     specs, constraints)


[
 to_colspec.when("dialect == 'jet' and isinstance(field, F.Entity)")]

def to_colspec(dialect, field):
    specs = []
    constraints = []
    for class_name in field.allow:
        col_name = '{table}_%s' % field._attribute
        if len(field.allow) > 1:
            col_name += '_%s' % class_name
        specs.append('`%s` INTEGER' % col_name)
        constraints.append('ALTER TABLE `{table}` ADD FOREIGN KEY (`%s`) REFERENCES %s (`%s_oid`);\n' % (
         col_name, class_name, class_name))

    return (specs, constraints)


[
 generic()]

def to_data(dialect, field):
    """Return a tuple of (col name, value) suitable for INSERT."""
    pass


[
 to_data.when("dialect == 'jet' and isinstance(field, F.Field)")]

def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '"%s"' % str(field).replace('"', '""')
        return (col_name, value)


[
 to_data.when("dialect == 'jet' and isinstance(field, F.Integer)")]

def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '%i' % field._value
        return (col_name, value)


[
 to_data.when("dialect == 'jet' and isinstance(field, F.Float)")]

def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '%f' % field._value
        return (col_name, value)


[
 to_data.when("dialect == 'jet' and isinstance(field, F.Money)")]

def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '%f' % field._value
        return (col_name, value)


[
 to_data.when("dialect == 'jet' and isinstance(field, F.Boolean)")]

def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        col_name = '`{table}_%s`' % field._attribute
        value = '%i' % field._value
        return (col_name, value)


[
 to_data.when("dialect == 'jet' and isinstance(field, F.Entity)")]

def to_data(dialect, field):
    if field._value is not UNASSIGNED:
        class_name = field._value.__class__.__name__
        col_name = field._attribute
        if len(field.allow) > 1:
            col_name += '_%s' % class_name
        col_name = '`{table}_%s`' % col_name
        value = '%i' % field._value.sys.oid
        return (col_name, value)