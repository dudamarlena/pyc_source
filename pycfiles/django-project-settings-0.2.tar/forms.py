# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-project-settings/project_settings/forms.py
# Compiled at: 2014-10-10 05:53:53
from __future__ import unicode_literals
from collections import defaultdict
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import urlize
from project_settings.models import Setting
from project_settings.registry import registry
from project_settings.conf import settings

class SettingsForm(forms.Form):
    """
    Form for settings - creates a field for each setting in
    ``mezzanine.conf`` that is marked as editable.
    """

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        settings.use_editable()
        for name in sorted(registry.keys()):
            setting = registry[name]
            if setting[b'editable']:
                field_class = type(setting[b'descriptor'].formfield)
                kwargs = {b'label': setting[b'label'] + b':', 
                   b'initial': getattr(settings, name), 
                   b'help_text': self.format_help(setting[b'description'])}
                if setting[b'choices']:
                    field_class = forms.ChoiceField
                    kwargs[b'choices'] = setting[b'choices']
                self.fields[name] = field_class(**kwargs)
                css_class = field_class.__name__.lower()
                self.fields[name].widget.attrs[b'class'] = css_class

    def __iter__(self):
        """
        Calculate and apply a group heading to each field and order by the
        heading.
        """
        fields = list(super(SettingsForm, self).__iter__())
        group = lambda field: field.name.split(b'_', 1)[0].title()
        misc = _(b'Miscellaneous')
        groups = defaultdict(int)
        for field in fields:
            groups[group(field)] += 1

        for i, field in enumerate(fields):
            setattr(fields[i], b'group', group(field))
            if groups[fields[i].group] == 1:
                fields[i].group = misc

        return iter(sorted(fields, key=lambda x: (x.group == misc, x.group)))

    def save(self):
        """
        Save each of the settings to the DB.
        """
        for name, value in self.cleaned_data.items():
            setting_obj, created = Setting.objects.get_or_create(name=name)
            setting_obj.value = value
            setting_obj.save()

    def format_help(self, description):
        """
        Format the setting's description into HTML.
        """
        for bold in ('``', '*'):
            parts = []
            if description is None:
                description = b''
            for i, s in enumerate(description.split(bold)):
                parts.append(s if i % 2 == 0 else b'<b>%s</b>' % s)

            description = (b'').join(parts)

        return mark_safe(urlize(description).replace(b'\n', b'<br>'))