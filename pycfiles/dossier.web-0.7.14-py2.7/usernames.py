# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/extraction/usernames.py
# Compiled at: 2015-09-05 21:24:22
from __future__ import absolute_import
import regex as re
from dossier.fc import StringCounter
from urlparse import urlparse
path_prefixes = 'user|users|Users|home|data/media|var/users|u01' + '|Documents and Settings|WINNT\\\\Profiles'
username_re = re.compile('^((?P<drive>[A-Za-z]):)?(/|\\\\)(%s)(/|\\\\)(?P<username>[^/\\\\$%%]+)' % path_prefixes)

def usernames(urls):
    """Take an iterable of `urls` of normalized URL or file paths and
    attempt to extract usernames.  Returns a list.

    """
    usernames = StringCounter()
    for url, count in urls.items():
        uparse = urlparse(url)
        path = uparse.path
        hostname = uparse.hostname
        m = username_re.match(path)
        if m:
            usernames[m.group('username')] += count
        elif hostname in ('twitter.com', 'www.facebook.com'):
            usernames[path.lstrip('/')] += count

    return usernames