# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/forms/fields.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import six
from django.forms.widgets import RadioFieldRenderer, TextInput, Widget
from django.forms.util import flatatt
from django.forms import Field, CharField, EmailField, TypedChoiceField, ValidationError
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from sentry.models import User
from sentry.security import is_valid_email_address

class CustomTypedChoiceField(TypedChoiceField):

    def validate(self, value):
        """
        Validates that the input is in self.choices.
        """
        super(CustomTypedChoiceField, self).validate(value)
        if value is not None and not self.valid_value(value):
            raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice', params={'value': value})
        return


class RadioFieldRenderer(RadioFieldRenderer):
    """
    This is identical to Django's builtin widget, except that
    it renders as a Bootstrap2 compatible widget. Would be great if
    we didn't have to create this stupid code, but Django widgets are not
    flexible.
    """

    def render(self):
        return mark_safe('\n<div class="inputs-list">%s</div>\n' % ('\n').join([ force_text(w) for w in self ]))


class UserField(CharField):

    class widget(TextInput):

        def render(self, name, value, attrs=None):
            if not attrs:
                attrs = {}
            if 'placeholder' not in attrs:
                attrs['placeholder'] = 'username'
            if isinstance(value, six.integer_types):
                value = User.objects.get(id=value).username
            return super(UserField.widget, self).render(name, value, attrs)

    def clean(self, value):
        value = super(UserField, self).clean(value)
        if not value:
            return
        else:
            try:
                return User.objects.get(username=value, is_active=True)
            except User.DoesNotExist:
                raise ValidationError(_('Invalid username'))

            return


class ReadOnlyTextWidget(Widget):

    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs)
        if not value:
            value = mark_safe('<em>%s</em>' % _('Not set'))
        return format_html('<div{0}>{1}</div>', flatatt(final_attrs), value)


class ReadOnlyTextField(Field):
    widget = ReadOnlyTextWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        super(ReadOnlyTextField, self).__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        return initial


def email_address_validator(value):
    if not is_valid_email_address(value):
        raise ValidationError(_('Enter a valid email address.'), code='invalid')
    return value


class AllowedEmailField(EmailField):
    default_validators = EmailField.default_validators + [email_address_validator]