# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/recaptcha/widgets.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.conf import settings
from django.forms import widgets
from django.utils.html import format_html

class RecaptchaWidget(widgets.Widget):
    """A widget for rendering the reCAPTCHA form field."""

    def render(self, *args, **kwargs):
        """Render the reCAPTCHA form field.

        Args:
            *args (tuple):
                Unused positional arguments.

            **kwargs (dict):
                Unused keyword arguments.

        Returns:
            django.utils.safestring.SafeText:
            The rendered reCAPTCHA widget.
        """
        return format_html(b'<div class="g-recaptcha" data-sitekey="{0}"></div>', settings.RECAPTCHA_PUBLIC_KEY)