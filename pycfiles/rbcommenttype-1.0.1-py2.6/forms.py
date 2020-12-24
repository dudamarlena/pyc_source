# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/rbcommenttype/forms.py
# Compiled at: 2015-12-14 18:14:24
from __future__ import unicode_literals
import json
from django.forms import BooleanField, Field, Widget
from django.forms.util import flatatt
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.forms import SettingsForm

class CommentTypesWidget(Widget):
    """A form widget for configuring comment types."""

    def render(self, name, value, attrs=None):
        """Render the widget."""
        attrs = self.build_attrs(attrs, type=b'hidden', name=name)
        if value:
            attrs[b'value'] = json.dumps(value)
        return format_html(b'<input{0} />', flatatt(attrs))


class CommentTypesField(Field):
    """A form field for configuring comment types."""
    widget = CommentTypesWidget

    def __init__(self, *args, **kwargs):
        """Initialize the field."""
        super(CommentTypesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """Return a python dictionary mapping ID to comment type."""
        return json.loads(value)


class CommentTypeSettingsForm(SettingsForm):
    """Settings form for comment type categorization."""
    require_type = BooleanField(initial=False, required=False, label=_(b'Require comment type'), help_text=_(b'Require users to select a comment type for every new comment.'))
    types = CommentTypesField(required=True)