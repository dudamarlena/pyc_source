# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbotext/widgets.py
# Compiled at: 2018-07-31 04:09:55
"""Special form widgets used in Review Bot."""
from __future__ import unicode_literals
import json
from django.forms.widgets import MultiWidget
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class ToolOptionsWidget(MultiWidget):
    """Widget for showing tool-specific options.

    Review Bot tools may define some tool-specific options that can be
    specified through the admin UI. Because tools are located on the worker
    nodes and the extension doesn't actually have their implementations, they
    communicate what options are available and what form fields should be used
    to configure them via a big JSON blob.
    """

    def __init__(self, tools, attrs=None):
        """Initialize the widget.

        Args:
            tools (list of reviewbotext.models.Tool):
                The list of tools.

            attrs (dict, optional):
                Additional attributes for the widget (unused).
        """
        self.fields = []
        for tool in tools:
            for option in tool.tool_options:
                field_class = self._import_class(option[b'field_type'])
                field_options = option.get(b'field_options', {})
                widget_def = option.get(b'widget')
                if widget_def is None:
                    widget = None
                else:
                    widget_class = self._import_class(widget_def[b'type'])
                    widget = widget_class(attrs=widget_def.get(b'attrs'))
                self.fields.append({b'tool_id': tool.pk, 
                   b'name': option[b'name'], 
                   b'default': option.get(b'default'), 
                   b'form_field': field_class(widget=widget, **field_options)})

        sub_widgets = [ field[b'form_field'].widget for field in self.fields ]
        super(ToolOptionsWidget, self).__init__(sub_widgets, attrs)
        return

    def _import_class(self, class_path):
        """Import and return a class.

        Args:
            class_path (unicode):
                The module path of the class to import.

        Returns:
            type:
            The imported class.
        """
        class_path = class_path.encode(b'ascii').split(b'.')
        if class_path:
            module_name = (b'.').join(class_path[:-1])
        else:
            module_name = b'.'
        module = __import__(module_name, {}, {}, class_path[(-1)])
        return getattr(module, class_path[(-1)])

    def render(self, name, value, attrs=None):
        """Render the widget.

        This overrides MultiWidget's rendering to render the sub-fields more
        like their own rows.

        Args:
            name (unicode):
                The name of the field.

            value (unicode):
                The current value of the field.

            attrs (dict, optional):
                Any attributes to include on the HTML element.

        Returns:
            django.utils.safestring.SafeText:
            The rendered widget.
        """
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized

        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get(b'id', None)
        assert len(self.widgets) == len(self.fields)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None

            if id_:
                final_attrs = dict(final_attrs, id=b'%s_%s' % (id_, i))
            widget_name = b'%s_%s' % (name, i)
            field = self.fields[i]
            if field[b'form_field'].required:
                label_class = b'required'
            else:
                label_class = b''
            if field[b'form_field'].help_text:
                help_text = format_html(b'<p class="help">{0}</p>', field[b'form_field'].help_text)
            else:
                help_text = b''
            output.append(format_html(b'<div class="form-row" data-tool-id="{tool_id}"      style="display: none;"> <label for="{widget_name}"         class="{label_class}">{field_label}:</label> {widget} {help_text}</div>', tool_id=field[b'tool_id'], field_label=field[b'form_field'].label, help_text=help_text, label_class=label_class, widget_name=widget_name, widget=widget.render(widget_name, widget_value, final_attrs)))

        return mark_safe(self.format_output(output))

    def value_from_datadict(self, data, files, name):
        """Return the value for this widget's field from the form data.

        Args:
            data (dict):
                The form data.

            files (dict):
                Any files submitted along with the form.

            name (unicode):
                The name of the current field.
        """
        selected_tool = int(data[b'tool'] or 0)
        result = {}
        for i, widget in enumerate(self.widgets):
            field = self.fields[i]
            if field[b'tool_id'] == selected_tool:
                key = field[b'name']
                value = widget.value_from_datadict(data, files, b'%s_%s' % (name, i))
                result[key] = value

        return json.dumps(result)

    def decompress(self, value):
        """Return an array of sub-field values given the field value.

        Args:
            value (unicode):
                The stored value for the top-level field.

        Returns:
            list:
            A list of values for each sub-widget.
        """
        if value:
            values = json.loads(value)
        else:
            values = {}
        return [ values.get(field[b'name'], field[b'default']) for field in self.fields ]