# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/command/search.py
# Compiled at: 2015-02-25 04:28:29
# Size of source mod 2**32: 1423 bytes
import sys, json, contextlib
from . import Command
from . import CommandError
from six.moves import urllib

class SearchCommand(Command):
    __doc__ = 'Search plugins in online repository'

    def print_item(self, item):
        sys.stdout.write('%(name)-20s %(description)s\n' % item)

    def execute(self):
        plugin_url = self.args.index_url or self.config.get('catalog.url', 'https://plugins.drove.io').strip('/')
        request = '%s/api/1/search?%s' % (
         plugin_url,
         urllib.parse.urlencode({'q': self.args.plugin}))
        try:
            with contextlib.closing(urllib.request.urlopen(request)) as (resp):
                obj = json.loads(resp.read().decode('utf-8'))
                if 'results' not in obj or not isinstance(obj['results'], list):
                    raise CommandError("Malformed response from '%s'" % (
                     plugin_url,))
                else:
                    if len(obj['results']) == 0:
                        self.log.warning('None plugin found')
                    else:
                        for result in obj['results']:
                            self.print_item(result)

        except BaseException as e:
            raise CommandError(str(e))