# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/admin/templatetags/admin_modify.py
# Compiled at: 2018-07-11 18:15:30
from django import template
register = template.Library()

@register.inclusion_tag('admin/prepopulated_fields_js.html', takes_context=True)
def prepopulated_fields_js(context):
    """
    Creates a list of prepopulated_fields that should render Javascript for
    the prepopulated fields for both the admin form and inlines.
    """
    prepopulated_fields = []
    if context['add'] and 'adminform' in context:
        prepopulated_fields.extend(context['adminform'].prepopulated_fields)
    if 'inline_admin_formsets' in context:
        for inline_admin_formset in context['inline_admin_formsets']:
            for inline_admin_form in inline_admin_formset:
                if inline_admin_form.original is None:
                    prepopulated_fields.extend(inline_admin_form.prepopulated_fields)

    context.update({'prepopulated_fields': prepopulated_fields})
    return context


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    ctx = {'opts': opts, 
       'onclick_attrib': opts.get_ordered_objects() and change and 'onclick="submitOrderForm();"' or '', 
       'show_delete_link': not is_popup and context['has_delete_permission'] and change and context.get('show_delete', True), 
       'show_save_as_new': not is_popup and change and save_as, 
       'show_save_and_add_another': context['has_add_permission'] and not is_popup and (not save_as or context['add']), 
       'show_save_and_continue': not is_popup and context['has_change_permission'], 
       'is_popup': is_popup, 
       'show_save': True}
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx


@register.filter
def cell_count(inline_admin_form):
    """Returns the number of cells used in a tabular inline"""
    count = 1
    for fieldset in inline_admin_form:
        for line in fieldset:
            for field in line:
                count += 1

    if inline_admin_form.formset.can_delete:
        count += 1
    return count