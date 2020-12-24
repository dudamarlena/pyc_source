# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/bugtracker.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from djblets.cache.backend import cache_memoize

class BugTracker(object):
    """An interface to a bug tracker.

    BugTracker subclasses are used to enable interaction with different
    bug trackers.
    """

    def get_bug_info(self, repository, bug_id):
        """Get the information for the specified bug.

        This should return a dictionary with 'summary', 'description', and
        'status' keys.

        This is cached for 60 seconds to reduce the number of queries to the
        bug trackers and make things seem fast after the first infobox load,
        but is still a short enough time to give relatively fresh data.
        """
        return cache_memoize(self.make_bug_cache_key(repository, bug_id), lambda : self.get_bug_info_uncached(repository, bug_id), expiration=60)

    def get_bug_info_uncached(self, repository, bug_id):
        """Get the information for the specified bug (implementation).

        This should be implemented by subclasses, and should return a
        dictionary with 'summary', 'description', and 'status' keys.
        If any of those are unsupported by the given bug tracker, the unknown
        values should be given as an empty string.
        """
        return {b'summary': b'', 
           b'description': b'', 
           b'status': b''}

    def make_bug_cache_key(self, repository, bug_id):
        """Returns a key to use when caching fetched bug information."""
        return b'repository-%s-bug-%s' % (repository.pk, bug_id)