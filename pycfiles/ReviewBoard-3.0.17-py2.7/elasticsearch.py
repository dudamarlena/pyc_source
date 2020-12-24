# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/search/search_backends/elasticsearch.py
# Compiled at: 2020-02-11 04:03:56
"""A backend for the Elasticsearch search engine."""
from __future__ import unicode_literals
from importlib import import_module
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
from reviewboard.search.search_backends.base import SearchBackend, SearchBackendForm

class ElasticsearchConfigForm(SearchBackendForm):
    """A form for configuring the Elasticsearch search backend."""
    url = forms.URLField(label=_(b'Elasticsearch URL'), help_text=_(b'The URL of the Elasticsearch server.'), widget=forms.TextInput(attrs={b'size': 80}))
    index_name = forms.CharField(label=_(b'Elasticsearch index name'), help_text=_(b'The name of the Elasticsearch index.'), widget=forms.TextInput(attrs={b'size': 40}))


class ElasticsearchBackend(SearchBackend):
    """A search backend for integrating with Elasticsearch"""
    search_backend_id = b'elasticsearch'
    name = _(b'Elasticsearch')
    haystack_backend_name = b'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine'
    default_settings = {b'URL': b'http://127.0.0.1:9200/', 
       b'INDEX_NAME': b'reviewboard'}
    config_form_class = ElasticsearchConfigForm
    form_field_map = {b'url': b'URL', 
       b'index_name': b'INDEX_NAME'}

    def validate(self):
        """Ensure that the elasticsearch Python module is installed.

        Raises:
            django.core.exceptions.ValidationError:
                Raised if the ``elasticsearch`` module is not installed.
        """
        try:
            module = import_module(b'elasticsearch')
        except ImportError:
            module = None

        if module is None or not hasattr(module, b'VERSION') or module.VERSION[0] > 2:
            raise ValidationError(ugettext(b'The elasticsearch 2.x Python module (and the Elasticsearch 2.x service) is required. The module can be installed by running: pip install "elasticsearch>=2.0,<3.0"'))
        return