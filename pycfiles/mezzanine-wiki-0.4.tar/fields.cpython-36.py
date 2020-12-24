# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\landon\dropbox\documents\pycharmprojects\mezzanine-wiki\mezzanine_wiki\fields.py
# Compiled at: 2018-02-16 21:21:46
# Size of source mod 2**32: 1032 bytes
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.utils.importing import import_dotted_path

class WikiTextField(models.TextField):
    __doc__ = '\n    TextField that stores markup text.\n    '

    def formfield(self, **kwargs):
        from mezzanine.conf import settings
        try:
            widget_class = import_dotted_path(settings.WIKI_TEXT_WIDGET_CLASS)
        except ImportError:
            raise ImproperlyConfigured(_('Could not import the value of settings.WIKI_TEXT_WIDGET_CLASS: %s' % settings.WIKI_TEXT_WIDGET_CLASS))

        kwargs['widget'] = widget_class()
        formfield = (super(WikiTextField, self).formfield)(**kwargs)
        return formfield