# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/search/search_backends/whoosh.py
# Compiled at: 2020-02-11 04:03:56
"""A backend for the Whoosh search engine."""
from __future__ import unicode_literals
import os
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from reviewboard.search.search_backends.base import SearchBackend, SearchBackendForm

class WhooshConfigForm(SearchBackendForm):
    """A form for configuring the Whoosh search backend."""
    search_index_file = forms.CharField(label=_(b'Search index directory'), help_text=_(b'The directory that search index data should be stored in.'), widget=forms.TextInput(attrs={b'size': b'80'}))

    def clean_search_index_file(self):
        """Clear the search_index_file field.

        This ensures the value is an absolute path and is writable.
        """
        index_file = self.cleaned_data[b'search_index_file'].strip()
        if index_file:
            if not os.path.isabs(index_file):
                raise ValidationError(_(b'The search index path must be absolute.'))
            if os.path.exists(index_file) and not os.access(index_file, os.W_OK):
                raise ValidationError(_(b'The search index path is not writable. Make sure the web server has write access to it and its parent directory.'))
        return index_file


class WhooshBackend(SearchBackend):
    """The Whoosh search backend."""
    search_backend_id = b'whoosh'
    name = _(b'Whoosh')
    haystack_backend_name = b'haystack.backends.whoosh_backend.WhooshEngine'
    config_form_class = WhooshConfigForm
    default_settings = {b'PATH': os.path.join(settings.SITE_DATA_DIR, b'search-index')}
    form_field_map = {b'search_index_file': b'PATH'}