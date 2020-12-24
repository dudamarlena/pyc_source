# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ao/social/interfaces.py
# Compiled at: 2010-03-23 14:22:02
from zope.interface import Interface

class IShortUrlHandler(Interface):
    """Interface for ShortUrlHandler objects."""

    def cache_context(url, context):
        """Cache the context (i.e. using memcache)."""
        pass

    def get_context_from_cache(url):
        """Look up the cached context."""
        pass

    def get_context_from_db(url):
        """Look up the context in the database."""
        pass

    def generate_url(len, elems):
        """Generate (a random) new url."""
        pass

    def assign_url(context):
        """Create a new URL for the context and assign it to the context."""
        pass

    def construct_url(context, request):
        """Construct the short url for the given context."""
        pass