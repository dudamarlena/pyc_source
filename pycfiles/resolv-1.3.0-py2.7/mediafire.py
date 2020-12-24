# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/resolv/resolvers/mediafire.py
# Compiled at: 2012-11-02 14:35:01
import re, urllib2
from resolv.shared import ResolverError, TechnicalError, unescape, Task

class MediafireTask(Task):
    result_type = 'file'
    name = 'MediaFire'
    author = 'Sven Slootweg'
    author_url = 'http://cryto.net/~joepie91'

    def run(self):
        url_match = re.match('(https?):\\/\\/(www\\.)?mediafire\\.com\\/view\\/\\?([a-z0-9]+)', self.url)
        if url_match is not None:
            self.url = '%s://%smediafire.com/?%s' % url_match.groups(1)
        url_match = re.match('(https?):\\/\\/(www\\.)?mediafire\\.com\\/\\?([a-z0-9]+)', self.url)
        if url_match is None:
            self.state = 'invalid'
            raise ResolverError('The specified URL is not a valid MediaFire URL.')
        try:
            contents = self.fetch_page(self.url)
        except urllib2.URLError as e:
            self.state = 'failed'
            raise TechnicalError('Could not retrieve the specified URL.')

        if '<form name="form_password"' in contents:
            self.state = 'need_password'
            return self
        else:
            return self._find_link(contents)
            return

    def verify_password(self, password):
        contents = self.post_page(self.url, {'downloadp': password})
        if '<form name="form_password"' in contents:
            self.state = 'password_invalid'
            return self
        else:
            return self._find_link(contents)

    def _find_link(self, contents):
        matches = re.search('kNO = "([^"]+)";', contents)
        if matches is None:
            self.state = 'failed'
            print contents
            raise ResolverError('No download was found on the given URL; the server for this file may be in maintenance mode, or the given URL may not be valid. It is also possible that you have been blocked - CAPTCHA support is not yet present.')
        file_url = matches.group(1)
        try:
            file_title = unescape(re.search('<title>([^<]+)<\\/title>', contents).group(1))
        except:
            self.state = 'failed'
            raise TechnicalError('Could not find the download title.')

        file_dict = {'url': file_url, 
           'method': 'GET', 
           'priority': 1, 
           'format': 'unknown'}
        self.results = {'title': file_title, 
           'files': [
                   file_dict]}
        self.state = 'finished'
        return self