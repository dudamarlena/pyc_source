# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/resolv/__init__.py
# Compiled at: 2012-11-02 14:35:01
import re, resolvers
from resolv.shared import ResolverError

def resolve(url):
    if re.match('https?:\\/\\/(www\\.)?putlocker\\.com', url) is not None:
        task = resolvers.PutlockerTask(url)
        return task.run()
    else:
        if re.match('https?:\\/\\/(www\\.)?sockshare\\.com', url) is not None:
            task = resolvers.SockshareTask(url)
            return task.run()
        if re.match('https?:\\/\\/(www\\.)?1channel\\.ch\\/external\\.php', url) is not None:
            task = resolvers.OneChannelTask(url)
            return task.run()
        if re.match('https?:\\/\\/(www\\.)?youtube\\.com\\/watch\\?', url) is not None:
            task = resolvers.YoutubeTask(url)
            return task.run()
        if re.match('https?:\\/\\/(www\\.)?filebox\\.com\\/[a-zA-Z0-9]+', url) is not None:
            task = resolvers.FileboxTask(url)
            return task.run()
        if re.match('https?:\\/\\/(www\\.)?vidxden\\.com\\/[a-zA-Z0-9]+', url) is not None:
            task = resolvers.VidxdenTask(url)
            return task.run()
        if re.match('https?:\\/\\/(www\\.)?vidbux\\.com\\/[a-zA-Z0-9]+', url) is not None:
            task = resolvers.VidbuxTask(url)
            return task.run()
        if re.match('https?:\\/\\/(www\\.)?filenuke\\.com\\/[a-zA-Z0-9]+', url) is not None:
            task = resolvers.FilenukeTask(url)
            return task.run()
        if re.match('https?:\\/\\/(www\\.)?pastebin\\.com\\/[a-zA-Z0-9]+', url) is not None:
            task = resolvers.PastebinTask(url)
            return task.run()
        if re.match('https?:\\/\\/(www\\.)?mediafire\\.com\\/(view\\/)?\\?[a-z0-9]+', url) is not None:
            task = resolvers.MediafireTask(url)
            return task.run()
        raise ResolverError('No suitable resolver found for %s' % url)
        return


def recurse(url):
    previous_result = {}
    while True:
        result = resolve(url)
        if result.state == 'failed':
            return previous_result
        if result.result_type != 'url':
            return result
        url = result.results['url']
        previous_result = result