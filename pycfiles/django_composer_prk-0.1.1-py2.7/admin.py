# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/admin.py
# Compiled at: 2017-10-20 11:35:08
import os, re
from django import forms
from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.template import loader
from django.template.loaders import app_directories
import nested_admin
from composer.models import Column, Row, Slot, Tile
from composer.templatetags.composer_tags import ComposerNode
from composer.utils import get_view_choices

class TileInlineForm(forms.ModelForm):

    class Meta:
        model = Tile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TileInlineForm, self).__init__(*args, **kwargs)
        self.fields['view_name'].widget = forms.widgets.Select(choices=[
         ('', '')] + get_view_choices())
        try:
            styles = list(settings.COMPOSER['styles'])
        except (AttributeError, KeyError):
            styles = []

        styles.append(('tile', 'Tile'))
        styles = self.get_existing_styles(styles)
        styles.sort()
        self.fields['style'].widget = forms.widgets.Select(choices=styles)

    def get_existing_styles(self, current_styles):
        """return list(tuple("key", "val"), ...)
        self -- current inline form instance.
        current_styles -- styles that are already present by default or
        obtained from other settings.

        If the settings are not present, it will return the list of already set
        styles, by default consisting only of [("tile", "Tile")].
        """
        try:
            setting = settings.COMPOSER
        except AttributeError:
            return current_styles

        if not setting.get('load-existing-styles'):
            return current_styles
        else:
            styles_settings = setting['load-existing-styles']
            greedy = styles_settings.get('greedy', False)
            excludes = styles_settings.get('excludes')
            includes = styles_settings.get('includes')
            if not greedy and excludes is None and includes is None:
                return []
            template_dirs = app_directories.get_app_template_dirs('templates')
            installed_apps = apps.app_configs.keys()
            template_dict = {}
            for app_dir in template_dirs:
                for path, dirnames, filenames in os.walk(app_dir):
                    if filenames and 'inclusion_tags' in path:
                        split = path.split('/')
                        if not split[(len(split) - 1)] == 'inclusion_tags':
                            continue
                        app_label = split[(len(split) - 2)]
                        for filename in filenames:
                            if len(filename.split('_')) > 1:
                                data = {'path': os.path.join(path, filename), 'filename': filename}
                                if template_dict.get(app_label, None) is None:
                                    template_dict[app_label] = []
                                template_dict[app_label].append(data)

            styles_dict = {}
            for model in apps.get_models():
                model_name = model._meta.model_name
                app_label = model._meta.app_label
                template_data = template_dict.get(app_label, None)
                if template_data is not None:
                    if not greedy:
                        if excludes:
                            to_exclude = excludes.get(app_label, [])
                            if to_exclude == '__all__' or model_name in to_exclude:
                                continue
                        if includes:
                            to_include = includes.get(app_label, [])
                            if to_include != '__all__' and model_name not in to_include:
                                continue
                    pattern = re.compile('%s_|\\.html' % model_name)
                    for template in template_data:
                        filename = template['filename']
                        path = template['path']
                        if '%s/inclusion_tags/%s_' % (app_label, model_name) in path:
                            style = pattern.sub('', filename)
                            if style not in styles_dict.keys():
                                styles_dict[style] = style.capitalize().replace('_', ' ')

            new_styles = [ (k, v) for k, v in styles_dict.iteritems() ]
            new_styles = set(current_styles + new_styles)
            return list(new_styles)


class TileInline(nested_admin.NestedTabularInline):
    model = Tile
    sortable_field_name = 'position'
    extra = 0
    form = TileInlineForm


class ColumnInline(nested_admin.NestedTabularInline):
    model = Column
    sortable_field_name = 'position'
    inlines = [TileInline]
    extra = 0


class RowInline(nested_admin.NestedTabularInline):
    model = Row
    sortable_field_name = 'position'
    inlines = [ColumnInline]
    extra = 0


class SlotAdminForm(forms.ModelForm):
    model = Slot

    def __init__(self, *args, **kwargs):
        """ Manipulate the form to provide a choice field for the slot name. We
        need to get the field choices from the base template. Doing this in the
        model init is wasteful, as we only need this when doing an admin edit.

        Also, it leads to circular imports.  An alternative could be to use the
        django.utils function lazy.
        """
        super(SlotAdminForm, self).__init__(*args, **kwargs)
        nodelist = loader.get_template('base.html').template.nodelist
        composer_nodes = nodelist.get_nodes_by_type(ComposerNode)
        slot_name_choices = [ [i.slot_name, i.slot_name] for i in composer_nodes
                            ]
        slot_name_help = self.fields['slot_name'].help_text
        self.fields['slot_name'] = forms.ChoiceField(help_text=slot_name_help, label='Slot Position', choices=slot_name_choices)
        if 'instance' not in kwargs and slot_name_choices:
            initial = slot_name_choices[0][0]
            for i, j in slot_name_choices:
                if i == 'content':
                    initial = i

            self.initial['slot_name'] = initial


class SlotAdmin(nested_admin.NestedModelAdmin):
    inlines = [
     RowInline]
    form = SlotAdminForm
    search_fields = [
     'title', 'url']
    list_filter = [
     'slot_name']
    ordering = [
     'url']


class TileAdmin(admin.ModelAdmin):
    list_display = ('_label', '_slot', '_slot_url')
    search_fields = [
     'column__row__slot__url', 'column__row__slot__title']
    list_filter = [
     'column__row__slot__slot_name']
    ordering = [
     'column__row__slot__url']

    def _label(self, obj):
        return obj.label

    def _slot(self, obj):
        return obj.column.row.slot.title

    def _slot_url(self, obj):
        return obj.column.row.slot.url


admin.site.register(Slot, SlotAdmin)
admin.site.register(Tile, TileAdmin)