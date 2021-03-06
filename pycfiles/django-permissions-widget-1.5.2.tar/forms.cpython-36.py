# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erik/src/django/swida/source/permissions_widget/forms.py
# Compiled at: 2017-09-11 12:49:25
# Size of source mod 2**32: 4783 bytes
"""
Form widget and field.

PermissionSelectMultipleField
    Permission field handling EXCLUDE_APPS and EXCLUDE_MODELS
    settings.

PermissionSelectMultipleWidget
    The actual permissions widget.
"""
from django import forms
from django import template
from django.db.models import Q
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Permission
from .settings import EXCLUDE_APPS, EXCLUDE_MODELS, APPS_ONLY, MODELS_ONLY, DEFAULT_PERMISSIONS

def filter_permissions(queryset):
    exclude_models_q = Q()
    for exclude_model in EXCLUDE_MODELS:
        app_label, model = exclude_model.split('.')
        exclude_models_q |= Q(content_type__app_label=app_label,
          content_type__model=model)

    queryset = queryset.exclude(Q(content_type__app_label__in=EXCLUDE_APPS) | exclude_models_q)
    include_models_q = Q()
    if MODELS_ONLY is not None:
        for include_model in MODELS_ONLY:
            app_label, model = include_model.split('.')
            include_models_q |= Q(content_type__app_label=app_label,
              content_type__model=model)

        queryset = queryset.filter(include_models_q)
    if APPS_ONLY is not None:
        queryset = queryset.filter(Q(content_type__app_label__in=APPS_ONLY))
    return queryset


class PermissionSelectMultipleWidget(forms.CheckboxSelectMultiple):
    __doc__ = '\n    Child of CheckboxSelectMultiple which renders\n    `permissions_widget/widget.html` to display the form field.\n    '
    custom_permission_types = []
    groups_permissions = []

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        t = get_template('permissions_widget/widget.html')
        c = {'name':name, 
         'value':value, 
         'table':self.get_table(), 
         'groups_permissions':self.groups_permissions, 
         'default_permission_types':DEFAULT_PERMISSIONS, 
         'custom_permission_types':self.custom_permission_types}
        ctx = template.Context(c)
        try:
            return mark_safe(t.render(ctx))
        except TypeError:
            return mark_safe(t.render(c))

    def get_table(self):
        table = []
        row = None
        last_app = None
        last_model = None
        try:
            permissions = self.choices.queryset
        except AttributeError:
            permissions = self.queryset

        for permission in permissions:
            codename = permission.codename
            model_part = '_' + permission.content_type.model
            permission_type = codename
            if permission_type.endswith(model_part):
                permission_type = permission_type[:-len(model_part)]
            app = permission.content_type.app_label
            model_class = permission.content_type.model_class()
            model_verbose_name = model_class._meta.verbose_name if model_class else None
            if permission_type not in list(DEFAULT_PERMISSIONS) + self.custom_permission_types:
                self.custom_permission_types.append(permission_type)
            is_app_or_model_different = last_model != model_class or last_app != app
            if is_app_or_model_different:
                row = dict(model=model_verbose_name, model_class=model_class, app=app, permissions={})
            row['permissions'][permission_type] = permission
            if is_app_or_model_different:
                table.append(row)
            last_app = app
            last_model = model_class

        return table


class PermissionSelectMultipleField(forms.ModelMultipleChoiceField):
    __doc__ = "\n    Simple child of forms.ModelMultipleChoiceField which pre-sets\n    queryset=Permission.objects.all(). It's an optional item here for your\n    convenience.\n    "
    widget = PermissionSelectMultipleWidget

    def __init__(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = Permission.objects.all()
        queryset = filter_permissions(queryset)
        (super(PermissionSelectMultipleField, self).__init__)(queryset, *args, **kwargs)

    def disable_group_permissions(self, user):
        if user.pk:
            self.widget.groups_permissions = Permission.objects.filter(group__user=user)