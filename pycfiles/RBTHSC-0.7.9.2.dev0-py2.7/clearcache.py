# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\commands\clearcache.py
# Compiled at: 2017-04-19 05:14:02
from rbtools.api.cache import clear_cache
from rbtools.commands import Command, Option

class ClearCache(Command):
    """Delete the HTTP cache used for the API."""
    name = 'clear-cache'
    author = 'The Review Board Project'
    description = 'Delete the HTTP cache used for the API.'
    option_list = [
     Option('--cache-location', dest='cache_location', metavar='FILE', config_key='CACHE_LOCATION', default=None, help='The file to use for the API cache database.', added_in='0.7.3')]

    def main(self):
        """Unlink the API cache's path."""
        if self.options.cache_location:
            clear_cache(self.options.cache_location)
        else:
            clear_cache()