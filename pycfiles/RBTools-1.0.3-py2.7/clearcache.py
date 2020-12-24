# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/clearcache.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals
from rbtools.api.cache import clear_cache
from rbtools.commands import Command, Option

class ClearCache(Command):
    """Delete the HTTP cache used for the API."""
    name = b'clear-cache'
    author = b'The Review Board Project'
    description = b'Delete the HTTP cache used for the API.'
    option_list = [
     Option(b'--cache-location', dest=b'cache_location', metavar=b'FILE', config_key=b'CACHE_LOCATION', default=None, help=b'The file to use for the API cache database.', added_in=b'0.7.3')]

    def main(self):
        """Unlink the API cache's path."""
        if self.options.cache_location:
            clear_cache(self.options.cache_location)
        else:
            clear_cache()