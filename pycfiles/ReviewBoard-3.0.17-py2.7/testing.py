# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/search/testing.py
# Compiled at: 2020-02-11 04:03:56
"""Search-related testing utilities."""
from __future__ import unicode_literals
from contextlib import contextmanager
from django.core.management import call_command
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.admin.siteconfig import load_site_config

def reindex_search():
    """Rebuild the search index."""
    call_command(b'rebuild_index', interactive=False)


@contextmanager
def search_enabled(on_the_fly_indexing=False):
    """Temporarily enable indexed search.

    Args:
        on_the_fly_indexing (bool, optional):
            Whether or not to enable on-the-fly indexing.
    """
    siteconfig = SiteConfiguration.objects.get_current()
    if on_the_fly_indexing:
        siteconfig.set(b'search_on_the_fly_indexing', True)
    siteconfig.set(b'search_enable', True)
    siteconfig.save()
    load_site_config()
    try:
        yield
    finally:
        if on_the_fly_indexing:
            siteconfig.set(b'search_on_the_fly_indexing', False)
        siteconfig.set(b'search_enable', False)
        siteconfig.save()
        load_site_config()