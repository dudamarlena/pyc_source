# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/urls/resolvers.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import threading
from django.core.urlresolvers import RegexURLResolver, clear_url_caches, get_resolver

class DynamicURLResolver(RegexURLResolver):
    """A URL resolver that allows for dynamically altering URL patterns.

    A standard RegexURLResolver expects that a list of URL patterns will
    be set once and never again change. In most applications, this is a
    good assumption. However, some that are more specialized may need
    to be able to swap in URL patterns dynamically. For example, those
    that can plug in third-party extensions.

    DynamicURLResolver makes it easy to add and remove URL patterns. Any
    time the list of URL patterns changes, they'll be immediately available
    for all URL resolution and reversing.

    The usage is very simple::

        dynamic_patterns = DynamicURLResolver()
        urlpatterns = [dynamic_patterns]

        dynamic_patterns.add_patterns([
            url(...),
            url(...),
        ])

    DynamicURLResolver will handle managing all the lookup caches to ensure
    that there won't be any stale entries affecting any dynamic URL patterns.
    """

    def __init__(self, regex=b'', app_name=None, namespace=None):
        super(DynamicURLResolver, self).__init__(regex=regex, urlconf_name=[], app_name=app_name, namespace=namespace)
        self._resolver_chain = None
        self._lock = threading.Lock()
        return

    @property
    def url_patterns(self):
        """Returns the current list of URL patterns.

        This is a simplified version of RegexURLResolver.url_patterns that
        simply returns the preset list of patterns. Unlike the original
        function, we don't care if the list is empty.
        """
        return self.urlconf_module

    def add_patterns(self, patterns):
        """Adds a list of URL patterns.

        The patterns will be made immediately available for use for any
        lookups or reversing.
        """
        self.url_patterns.extend(patterns)
        self._repopulate_caches()

    def remove_patterns(self, patterns):
        """Removes a list of URL patterns.

        These patterns will no longer be able to be looked up or reversed.
        """
        for pattern in patterns:
            try:
                self.url_patterns.remove(pattern)
            except ValueError:
                pass

        self._repopulate_caches()

    def _repopulate_caches(self):
        """Repopulates the internal resolver caches.

        This will force all the resolvers in the chain to repopulate,
        replacing the caches, in order to ensure that the next lookup or
        reverse will result in a lookup in this resolver. By default, every
        RegexURLResolver in Django will cache all results from its children.

        We take special care to only repopulate the caches of the resolvers in
        our parent chain.
        """
        with self._lock:
            for resolver in self.resolver_chain:
                resolver._reverse_dict = {}
                resolver._namespace_dict = {}
                resolver._app_dict = {}
                resolver._callback_strs = set()
                resolver._populated = False

            clear_url_caches()

    @property
    def resolver_chain(self):
        """Returns every RegexURLResolver between here and the root.

        The list of resolvers is cached in order to prevent having to locate
        the resolvers more than once.
        """
        if self._resolver_chain is None:
            self._resolver_chain = self._find_resolver_chain(get_resolver(None))
        return self._resolver_chain

    def _find_resolver_chain(self, resolver):
        if resolver == self:
            return [resolver]
        for url_pattern in resolver.url_patterns:
            if isinstance(url_pattern, RegexURLResolver):
                resolvers = self._find_resolver_chain(url_pattern)
                if resolvers:
                    resolvers.append(resolver)
                    return resolvers

        return []