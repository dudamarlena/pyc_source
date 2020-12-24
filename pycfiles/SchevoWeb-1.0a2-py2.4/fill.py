# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/schevoweb/form/fill.py
# Compiled at: 2006-09-08 16:55:59
"""Fill in HTTP forms.

For copyright, license, and warranty, see bottom of file.
"""
import dispatch, elementtree.ElementTree as etree
from schevo import base
from schevo.constant import UNASSIGNED
from schevo.label import label
from schevo import field as F
from schevo import query

@dispatch.generic()
def fill(db, obj, tree, errors=None, prefix='', **options):
    """Return a filled-in HTML tree based on object values.

    Note: `fill` is destructive in nature and calls itself
    recursively; if you do not want your original template tree
    altered, make a copy of it to pass into `fill`.

    - `db`: The Schevo database being used.
    
    - `obj`: The Schevo object on which to read data.
    
    - `tree`: HTML string or ElementTree to fill.
    
    - `errors`: Optional dictionary of errors. Keys are field names,
      with a special key of '__form__' for form-level errors.  Values
      are error message strings or tuples of (error message,
      exception).

    - `prefix`: The prefix that field names start with when referenced
      in HTML.

    - `options`: Additional options that are used for specific field
      types.
    """
    pass


def _chop_prefix(name, prefix):
    if prefix and name.startswith(prefix):
        name = name[len(prefix):]
    return name


def _init_fill(tree, errors):
    """Convert tree to an Element if it is a string, and convert
    errors from None to an empty dictionary."""
    if isinstance(tree, basestring):
        tree = etree.fromstring(tree)
    if errors is None:
        errors = {}
    return (
     tree, errors)


@fill.when('isinstance(obj, query.Simple)')
def fill_simple(db, obj, tree, errors=None, prefix='', **options):
    (tree, errors) = _init_fill(tree, errors)
    return tree


@fill.when('isinstance(obj, query.Intersection)')
def fill_intersection(db, obj, tree, errors=None, prefix='', **options):
    (tree, errors) = _init_fill(tree, errors)
    index = 0
    for subquery in obj.queries:
        subprefix = '%s%i.' % (prefix, index)
        fill(db, subquery, tree, errors, subprefix, **options)
        index += 1

    return tree


@fill.when('isinstance(obj, query.Match)')
def fill_match(db, obj, tree, errors=None, prefix='', **options):
    (tree, errors) = _init_fill(tree, errors)
    for tag in tree.getiterator('select'):
        name = tag.get('name', None)
        if name:
            name = _chop_prefix(name, prefix)
            if name == 'operator':
                for operator in obj.valid_operators:
                    option = etree.SubElement(tag, 'option')
                    option.set('value', operator.name)
                    option.text = label(operator)
                    if operator is obj.operator:
                        option.set('selected', 'yes')

    field = obj.FieldClass(obj, 'value')
    field.required = False
    if obj.value is not None:
        field.assign(obj.value)
    fill(db, field, tree, errors, prefix, **options)
    return tree


@fill.when('isinstance(obj, F.Field)')
def fill_field(db, obj, tree, errors=None, prefix='', **options):
    (tree, errors) = _init_fill(tree, errors)
    for tag in tree.getiterator('input'):
        name = tag.get('name', None)
        if name:
            name = _chop_prefix(name, prefix)
            if name == obj.name:
                reversible = obj.reversible()
                if tag.get('type', None) == 'radio':
                    if tag.get('value', None) == reversible:
                        tag.set('checked', 'yes')
                else:
                    tag.set('value', reversible)

    for tag in tree.getiterator('textarea'):
        name = tag.get('name', None)
        if name:
            name = _chop_prefix(name, prefix)
            if name == obj.name:
                text = obj.reversible()
                tag.text = text

    return tree


@fill.when('isinstance(obj, F.Entity)')
def fill_field_entity(db, obj, tree, errors=None, prefix='', **options):
    (tree, errors) = _init_fill(tree, errors)
    for tag in tree.getiterator('select'):
        name = tag.get('name', None)
        if name:
            name = _chop_prefix(name, prefix)
            if name == obj.name:
                current = obj.reversible()
                if not obj.required:
                    option = etree.SubElement(tag, 'option')
                    option.set('value', '')
                    if current == '':
                        option.set('selected', 'yes')
                valid_values = obj.valid_values
                if valid_values is None:
                    valid_values = []
                    for extent_name in obj.allow:
                        extent = db.extent(extent_name)
                        valid_values.extend(extent)

                for valid_value in valid_values:
                    value = '%s-%i' % (valid_value.sys.extent.name, valid_value.sys.oid)
                    value_label = label(valid_value)
                    option = etree.SubElement(tag, 'option')
                    option.set('value', value)
                    option.text = value_label
                    if value == current:
                        option.set('selected', 'yes')

    return tree


@fill.when('isinstance(obj, base.classes_using_fields)')
def fill_fields(db, obj, tree, errors=None, prefix='', **options):
    (tree, errors) = _init_fill(tree, errors)

    def _process(tag):
        for child in tag.getchildren():
            errorFor = child.get('errorFor', None)
            if errorFor is not None:
                if errorFor in errors:
                    del child.attrib['errorFor']
                    error = errors[errorFor]
                    if not isinstance(error, basestring):
                        error = error[0]
                    child.text = error
                else:
                    tag.remove(child)
            else:
                _process(child)

        return

    _process(tree)
    f = obj.f
    for tag in tree.getiterator('span'):
        name = tag.get('name', None)
        if name:
            name = _chop_prefix(name, prefix)
            if name in f:
                value = f[name].get()
                value_label = unicode(f[name])
                if value is UNASSIGNED:
                    tag.set('class', 'unassigned')
                lines = value_label.splitlines()
                if not lines:
                    tag.text = ''
                tag.text = lines[0]
                for line in lines[1:]:
                    br = etree.SubElement(tag, 'br')
                    br.tail = line

                del tag.attrib['name']

    for tag in tree.getiterator('input'):
        name = tag.get('name', None)
        if name:
            name = _chop_prefix(name, prefix)
            if name in f:
                rev = f[name].reversible()
                if tag.get('type', None) == 'radio':
                    if tag.get('value', None) == rev:
                        tag.set('checked', 'yes')
                else:
                    tag.set('value', rev)
            if name.startswith('_unassigned_'):
                name = name[len('_unassigned_'):]
                if name in f and tag.get('type', None) == 'checkbox':
                    if f[name].get() is UNASSIGNED:
                        tag.set('checked', 'yes')
            if name.startswith('_assigned_'):
                name = name[len('_assigned_'):]
                if name in f and tag.get('type', None) == 'checkbox':
                    if f[name].assigned:
                        tag.set('checked', 'yes')

    for tag in tree.getiterator('textarea'):
        name = tag.get('name', None)
        if name:
            name = _chop_prefix(name, prefix)
            if name in f:
                text = f[name].reversible()
                tag.text = text

    for tag in tree.getiterator('select'):
        name = tag.get('name', None)
        if name:
            name = _chop_prefix(name, prefix)
            if name in f:
                field = f[name]
                if isinstance(field, F.Entity):
                    current = field.reversible()
                    if not field.required:
                        option = etree.SubElement(tag, 'option')
                        option.set('value', '')
                        if current == '':
                            option.set('selected', 'yes')
                    valid_values = field.valid_values
                    if valid_values is None:
                        valid_values = []
                        for extent_name in field.allow:
                            extent = db.extent(extent_name)
                            valid_values.extend(extent)

                    for valid_value in valid_values:
                        value = '%s-%i' % (valid_value.sys.extent.name, valid_value.sys.oid)
                        value_label = label(valid_value)
                        option = etree.SubElement(tag, 'option')
                        option.set('value', value)
                        option.text = value_label
                        if value == current:
                            option.set('selected', 'yes')

                elif isinstance(field, F.Integer) and None not in (field.max_value, field.min_value):
                    current = field.reversible()
                    if not field.required:
                        option = etree.SubElement(tag, 'option')
                        option.set('value', '')
                        if current == '':
                            option.set('selected', 'yes')
                    value = field.min_value
                    while value <= field.max_value:
                        option = etree.SubElement(tag, 'option')
                        option.set('value', str(value))
                        option.text = str(value)
                        if str(value) == current:
                            option.set('selected', 'yes')
                        value += 1

    return tree