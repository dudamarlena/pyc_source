# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/resolv/resolvers/pastebin.py
# Compiled at: 2012-10-28 17:13:06
import re, urllib2
from resolv.shared import ResolverError, unescape, Task

class PastebinTask(Task):
    result_type = 'text'
    name = 'Pastebin'
    author = 'Sven Slootweg'
    author_url = 'http://cryto.net/~joepie91'

    def run(self):
        matches = re.search('https?:\\/\\/(www\\.)?pastebin\\.com\\/([a-zA-Z0-9]+)', self.url)
        if matches is None:
            self.state = 'invalid'
            raise ResolverError('The provided URL is not a valid Pastebin URL.')
        paste_id = matches.group(2)
        try:
            contents = self.fetch_page(self.url)
        except urllib2.URLError as e:
            self.state = 'failed'
            raise ResolverError('Could not retrieve the specified URL. The paste may not exist.')

        matches = re.search('<h1>([^<]+)</h1>', contents)
        if matches is None:
            self.state = 'invalid'
            raise ResolverError('The provided URL is not a valid paste.')
        paste_title = unescape(matches.group(1))
        resolved = {'url': 'http://pastebin.com/download.php?i=%s' % paste_id, 
           'method': 'GET', 
           'priority': 1, 
           'format': 'text'}
        self.results = {'title': paste_title, 
           'files': [
                   resolved]}
        self.state = 'finished'
        return self