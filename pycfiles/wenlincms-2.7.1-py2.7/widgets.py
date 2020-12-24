# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/boot/updates/contrib/admin/widgets.py
# Compiled at: 2016-05-20 23:42:06
"""
Form Widget classes specific to the Django admin site.
"""
from __future__ import unicode_literals
import copy
from django import forms
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse
from django.forms.util import flatatt
from django.forms.widgets import RadioFieldRenderer
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import escape, format_html, format_html_join, smart_urlquote
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.utils.translation import ugettext as _

class FilteredSelectMultiple(forms.SelectMultiple):
    """
    A SelectMultiple with a JavaScript filter interface.

    Note that the resulting JavaScript assumes that the jsi18n
    catalog has been loaded in the page
    """

    @property
    def media(self):
        js = [b'core.js', b'SelectBox.js', b'SelectFilter2.js']
        return forms.Media(js=[ static(b'admin/js/%s' % path) for path in js ])

    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        self.verbose_name = verbose_name
        self.is_stacked = is_stacked
        super(FilteredSelectMultiple, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        if attrs is None:
            attrs = {}
        attrs[b'class'] = b'selectfilter'
        if self.is_stacked:
            attrs[b'class'] += b'stacked'
        output = [
         super(FilteredSelectMultiple, self).render(name, value, attrs, choices)]
        output.append(b'<script type="text/javascript">addEvent(window, "load", function(e) {')
        output.append(b'SelectFilter.init("id_%s", "%s", %s, "%s"); });</script>\n' % (
         name, self.verbose_name.replace(b'"', b'\\"'), int(self.is_stacked), static(b'admin/')))
        return mark_safe((b'').join(output))


class AdminDateWidget(forms.DateInput):

    @property
    def media(self):
        js = [b'calendar.js', b'admin/DateTimeShortcuts.js']
        return forms.Media(js=[ static(b'admin/js/%s' % path) for path in js ])

    def __init__(self, attrs=None, format=None):
        final_attrs = {b'class': b'vDateField', b'size': b'10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminDateWidget, self).__init__(attrs=final_attrs, format=format)
        return


class AdminTimeWidget(forms.TimeInput):

    @property
    def media(self):
        js = [b'calendar.js', b'admin/DateTimeShortcuts.js']
        return forms.Media(js=[ static(b'admin/js/%s' % path) for path in js ])

    def __init__(self, attrs=None, format=None):
        final_attrs = {b'class': b'vTimeField', b'size': b'8'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTimeWidget, self).__init__(attrs=final_attrs, format=format)
        return


class AdminSplitDateTime(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """

    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return format_html(b'<p class="datetime">{0} {1}<br />{2} {3}</p>', _(b'Date:'), rendered_widgets[0], _(b'Time:'), rendered_widgets[1])


class AdminRadioFieldRenderer(RadioFieldRenderer):

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return format_html(b'<ul{0}>\n{1}\n</ul>', flatatt(self.attrs), format_html_join(b'\n', b'<li>{0}</li>', ((force_text(w),) for w in self)))


class AdminRadioSelect(forms.RadioSelect):
    renderer = AdminRadioFieldRenderer


class AdminFileWidget(forms.ClearableFileInput):
    template_with_initial = b'<p class="file-upload zd-upload">%s</p>' % forms.ClearableFileInput.template_with_initial
    template_with_clear = b'<span class="clearable-file-input">%s</span>' % forms.ClearableFileInput.template_with_clear


def url_params_from_lookup_dict(lookups):
    """
    Converts the type of lookups specified in a ForeignKey limit_choices_to
    attribute to a dictionary of query parameters
    """
    params = {}
    if lookups and hasattr(lookups, b'items'):
        items = []
        for k, v in lookups.items():
            if callable(v):
                v = v()
            if isinstance(v, (tuple, list)):
                v = (b',').join([ str(x) for x in v ])
            elif isinstance(v, bool):
                v = ('0', '1')[v]
            else:
                v = six.text_type(v)
            items.append((k, v))

        params.update(dict(items))
    return params


class ForeignKeyRawIdWidget(forms.TextInput):
    """
    A Widget for displaying ForeignKeys in the "raw_id" interface rather than
    in a <select> box.
    """

    def __init__(self, rel, admin_site, attrs=None, using=None):
        self.rel = rel
        self.admin_site = admin_site
        self.db = using
        super(ForeignKeyRawIdWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rel_to = self.rel.to
        if attrs is None:
            attrs = {}
        extra = []
        if rel_to in self.admin_site._registry:
            related_url = reverse(b'admin:%s_%s_changelist' % (
             rel_to._meta.app_label,
             rel_to._meta.model_name), current_app=self.admin_site.name)
            params = self.url_parameters()
            if params:
                url = b'?' + (b'&amp;').join([ b'%s=%s' % (k, v) for k, v in params.items() ])
            else:
                url = b''
            if b'class' not in attrs:
                attrs[b'class'] = b'vForeignKeyRawIdAdminField'
            extra.append(b'<a href="%s%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);"> ' % (
             related_url, url, name))
            extra.append(b'<img src="%s" width="16" height="16" alt="%s" /></a>' % (
             static(b'admin/img/selector-search.gif'), _(b'Lookup')))
        output = [
         super(ForeignKeyRawIdWidget, self).render(name, value, attrs)] + extra
        if value:
            output.append(self.label_for_value(value))
        return mark_safe((b'').join(output))

    def base_url_parameters(self):
        return url_params_from_lookup_dict(self.rel.limit_choices_to)

    def url_parameters(self):
        from django.contrib.admin.views.main import TO_FIELD_VAR
        params = self.base_url_parameters()
        params.update({TO_FIELD_VAR: self.rel.get_related_field().name})
        return params

    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.to._default_manager.using(self.db).get(**{key: value})
            return b'&nbsp;<strong>%s</strong>' % escape(Truncator(obj).words(14, truncate=b'...'))
        except (ValueError, self.rel.to.DoesNotExist):
            return b''


class ManyToManyRawIdWidget(ForeignKeyRawIdWidget):
    """
    A Widget for displaying ManyToMany ids in the "raw_id" interface rather than
    in a <select multiple> box.
    """

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        if self.rel.to in self.admin_site._registry:
            attrs[b'class'] = b'vManyToManyRawIdAdminField'
        if value:
            value = (b',').join([ force_text(v) for v in value ])
        else:
            value = b''
        return super(ManyToManyRawIdWidget, self).render(name, value, attrs)

    def url_parameters(self):
        return self.base_url_parameters()

    def label_for_value(self, value):
        return b''

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(b',')


class RelatedFieldWidgetWrapper(forms.Widget):
    """
    This class is a wrapper to a given widget to add the add icon for the
    admin interface.
    """

    def __init__(self, widget, rel, admin_site, can_add_related=None):
        self.is_hidden = widget.is_hidden
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.widget = widget
        self.rel = rel
        if can_add_related is None:
            can_add_related = rel.to in admin_site._registry
        self.can_add_related = can_add_related
        self.admin_site = admin_site
        return

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.widget = copy.deepcopy(self.widget, memo)
        obj.attrs = self.widget.attrs
        memo[id(self)] = obj
        return obj

    @property
    def media(self):
        return self.widget.media

    def render(self, name, value, *args, **kwargs):
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.model_name)
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if self.can_add_related:
            related_url = reverse(b'admin:%s_%s_add' % info, current_app=self.admin_site.name)
            output.append(b'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % (
             related_url, name))
            output.append(b'<img src="%s" width="10" height="10" alt="%s"/></a>' % (
             static(b'admin/img/icon_addlink.gif'), _(b'Add Another')))
        return mark_safe((b'').join(output))

    def build_attrs(self, extra_attrs=None, **kwargs):
        """Helper function for building an attribute dictionary."""
        self.attrs = self.widget.build_attrs(extra_attrs=None, **kwargs)
        return self.attrs

    def value_from_datadict(self, data, files, name):
        return self.widget.value_from_datadict(data, files, name)

    def id_for_label(self, id_):
        return self.widget.id_for_label(id_)


class AdminTextareaWidget(forms.Textarea):

    def __init__(self, attrs=None):
        final_attrs = {b'class': b'vLargeTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTextareaWidget, self).__init__(attrs=final_attrs)
        return


class AdminTextInputWidget(forms.TextInput):

    def __init__(self, attrs=None):
        final_attrs = {b'class': b'vTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTextInputWidget, self).__init__(attrs=final_attrs)
        return


class AdminEmailInputWidget(forms.EmailInput):

    def __init__(self, attrs=None):
        final_attrs = {b'class': b'vTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminEmailInputWidget, self).__init__(attrs=final_attrs)
        return


class AdminURLFieldWidget(forms.URLInput):

    def __init__(self, attrs=None):
        final_attrs = {b'class': b'vURLField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminURLFieldWidget, self).__init__(attrs=final_attrs)
        return

    def render(self, name, value, attrs=None):
        html = super(AdminURLFieldWidget, self).render(name, value, attrs)
        if value:
            value = force_text(self._format_value(value))
            final_attrs = {b'href': smart_urlquote(value)}
            html = format_html(b'<p class="url">{0} <a{1}>{2}</a><br />{3} {4}</p>', _(b'Currently:'), flatatt(final_attrs), value, _(b'Change:'), html)
        return html


class AdminIntegerFieldWidget(forms.TextInput):
    class_name = b'vIntegerField'

    def __init__(self, attrs=None):
        final_attrs = {b'class': self.class_name}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminIntegerFieldWidget, self).__init__(attrs=final_attrs)
        return


class AdminBigIntegerFieldWidget(AdminIntegerFieldWidget):
    class_name = b'vBigIntegerField'


class AdminCommaSeparatedIntegerFieldWidget(forms.TextInput):

    def __init__(self, attrs=None):
        final_attrs = {b'class': b'vCommaSeparatedIntegerField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminCommaSeparatedIntegerFieldWidget, self).__init__(attrs=final_attrs)
        return