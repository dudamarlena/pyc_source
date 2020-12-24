# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/schevoweb/form/template.py
# Compiled at: 2006-09-08 16:55:59
"""Create HTTP forms suitable for passing to ``schevoweb.form.fill``.

For copyright, license, and warranty, see bottom of file.
"""
from cgi import escape
import elementtree.ElementTree as etree, dispatch, dispatch.strategy
from schevo import base
from schevo.constant import UNASSIGNED
from schevo import field as F
from schevo.label import label
from schevo import query

@dispatch.generic()
def form_template(db, obj, prefix='', outer=True, **options):
    """Return a HTML string suitable for passing as a template to
    ``schevoweb.form.fill``.  Intended to be enclosed inside a
    ``form`` tag."""
    pass


@dispatch.generic()
def field_template(db, obj, field, id, **options):
    """Return a HTML template for a specific field."""
    pass


@form_template.when(dispatch.strategy.default)
def form_template_default(db, obj, prefix='', outer=True, **options):
    src = '<div>A form is not yet available for %s</div>' % escape(repr(obj))
    return etree.fromstring(src)


@form_template.when('isinstance(obj, base.classes_using_fields)')
def form_template_fields(db, obj, prefix='', outer=True, **options):
    form = []
    form.append('<div class="schevoForm">')
    if outer:
        form.append('<span errorFor="__form__" class="schevoFormError" />')
    f = obj.f
    auto_unset_unassigned = options.get('auto_unset_unassigned', False)
    for name in f:
        field = f[name]
        if field.hidden:
            continue
        if auto_unset_unassigned and not field.readonly and not field.required:
            unassigned_checkbox_id = '_unassigned_%s' % name
            if prefix:
                unassigned_checkbox_id = prefix + unassigned_checkbox_id
            options['field_javascript'] = 'onChange="getElementById(\'%s\').checked = false;"' % unassigned_checkbox_id
        field_label = escape(label(field))
        id = prefix + name
        form.append('<div class="schevoFormField">')
        form.append('<label for="%s">%s</label>' % (id, field_label))
        form.append('<span class="schevoFormFieldValue">')
        f_template = field_template(db, obj, field, id, **options)
        form.append(etree.tostring(f_template))
        form.append('</span>')
        form.append('<span errorFor="%s" class="schevoFormFieldError" />' % id)
        checkboxes = []
        assigned = options.get('assigned', None)
        if assigned:
            checkboxes.append(_checkbox('assigned', name, prefix, assigned))
        unassigned = options.get('unassigned', None)
        if unassigned and not field.readonly and not field.required:
            checkboxes.append(_checkbox('unassigned', name, prefix, unassigned))
        if checkboxes:
            form.append('<span class="schevoFormFieldOptions">')
            form.extend(checkboxes)
            form.append('</span>')
        form.append('</div>')

    form.append('</div>')
    src = ('\n').join(form)
    return etree.fromstring(src)


@form_template.when('isinstance(obj, query.Simple)')
def form_template_simple(db, obj, prefix='', outer=True, **options):
    form = etree.Element('div', **{'class': 'schevoForm'})
    if outer:
        form.append(etree.Element('span', **{'errorFor': '__form__', 'class': 'schevoFormError'}))
    form.text = '(No criteria.)'
    return form


@form_template.when('isinstance(obj, query.Intersection)')
def form_template_intersection(db, obj, prefix='', outer=True, **options):
    form = etree.Element('div', **{'class': 'schevoForm'})
    if outer:
        form.append(etree.Element('span', **{'errorFor': '__form__', 'class': 'schevoFormError'}))
    fieldset = etree.Element('fieldset')
    legend = etree.Element('legend')
    legend.text = label(obj)
    fieldset.append(legend)
    form.append(fieldset)
    index = 0
    for subquery in obj.queries:
        subprefix = '%s%i.' % (prefix, index)
        fieldset.append(form_template(db, subquery, prefix=subprefix, outer=False, **options))
        index += 1

    return form


@form_template.when('isinstance(obj, query.Match)')
def form_template_match(db, obj, prefix='', outer=True, **options):
    value_id = prefix + 'value'
    operator_id = prefix + 'operator'
    form = etree.Element('div', **{'class': 'schevoFormField'})
    label_elem = etree.Element('label', **{'for': value_id})
    label_elem.text = label(obj.FieldClass)
    form.append(label_elem)
    oper_span = etree.Element('span', **{'class': 'schevoFormFieldOperator'})
    oper_span.append(etree.Element('select', name=operator_id, id=operator_id))
    form.append(oper_span)
    value_span = etree.Element('span', **{'class': 'schevoFormFieldValue'})
    field = obj.FieldClass(None, value=obj.value)
    value_span.append(field_template(db, obj, field, value_id, **options))
    form.append(value_span)
    return form


@field_template.when('field.readonly')
def field_template_readonly(db, obj, field, id, **options):
    src = '<span id="%s" name="%s" />' % (id, id)
    return etree.fromstring(src)


@field_template.when('field.readonly and isinstance(field, F.Entity)')
def field_template_readonly_entity(db, obj, field, id, **options):
    entity_view_url = options.get('entity_view_url', None)
    field_value = field.get()
    if not entity_view_url or field_value is UNASSIGNED:
        return field_template_readonly(db, obj, field, id, **options)
    view_url = entity_view_url(field_value)
    inner = '<span id="%s" name="%s" />' % (id, id)
    entity_icon_url = options.get('entity_icon_url', None)
    icon_size = options.get('icon_size', None)
    if entity_icon_url and icon_size:
        icon_url = entity_icon_url(field_value)
        inner = '<img src="%s" height="%i" width="%i" /> %s' % (icon_url, icon_size, icon_size, inner)
    src = '<a href="%s">%s</a>' % (view_url, inner)
    return etree.fromstring(src)


@field_template.when('not field.readonly and isinstance(field, F.Field)')
def field_template_field(db, obj, field, id, **options):
    field_javascript = options.get('field_javascript', '')
    src = '<input id="%s" type="text" name="%s" %s />' % (id, id, field_javascript)
    return etree.fromstring(src)


@field_template.when('not field.readonly and isinstance(field, F.Boolean)')
def field_template_boolean(db, obj, field, id, **options):
    field_javascript = options.get('field_javascript', '')
    src = ''
    for (suffix, label) in [('true', field.true_label), ('false', field.false_label)]:
        src += '<input type="radio" id="%s_%s" name="%s" value="%s" %s>%s</input>' % (id, suffix, id, label, field_javascript, label)

    return etree.fromstring('<span>%s</span>' % src)


@field_template.when('not field.readonly and isinstance(field, F.Entity)')
def field_template_entity(db, obj, field, id, **options):
    field_javascript = options.get('field_javascript', '')
    src = '<select id="%s" name="%s" %s />' % (id, id, field_javascript)
    return etree.fromstring(src)


@field_template.when('not field.readonly and isinstance(field, F.Memo)')
def field_template_memo(db, obj, field, id, **options):
    field_javascript = options.get('field_javascript', '')
    src = '<textarea id="%s" name="%s" %s />' % (id, id, field_javascript)
    return etree.fromstring(src)


def _checkbox(type, name, prefix, label):
    id = '_%s_%s' % (type, name)
    if prefix:
        id = prefix + id
    return '<input id="%(id)s" type="checkbox" name="%(id)s" /><label for="%(id)s">%(label)s</label>' % vars()