# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/recaptcha/templatetags/djblets_recaptcha.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django import template
from django.utils.html import mark_safe
register = template.Library()

@register.simple_tag
def recaptcha_js():
    """Render the reCAPTCHA JavaScript tag.

    Returns:
        django.utils.safestring.SafeText:
        The rendered tag.
    """
    return mark_safe(b'<script src="https://www.google.com/recaptcha/api.js"></script>')


@register.simple_tag
def recaptcha_form_field(form):
    """Return the reCAPTCHA field from the specified form.

    This can be used to render the reCAPTCHA widget.

    Args:
        form (django.forms.forms.Form):
            The form that is being rendered.

    Returns:
        django.forms.boundfield.BoundField:
        The bound reCAPTCHA field. This will render as its widget in a
        template.
    """
    return form[b'g-recaptcha-response']