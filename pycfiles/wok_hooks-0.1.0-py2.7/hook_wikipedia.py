# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wok_hooks/hook_wikipedia.py
# Compiled at: 2014-10-09 05:39:56
import logging
from wok_hooks.misc import Configuration as _Configuration
import feedparser, datetime
from wok_hooks.timeline import Post as TimelineUpdate

class Configuration(_Configuration):
    DEFAULTS = {'lang': '', 'user': ''}

    def __init__(self, path, **kwargs):
        _Configuration.__init__(self, path, **kwargs)
        for key, value in Configuration.DEFAULTS.items():
            if key not in self:
                self[key] = value
                self.save()


class WikipediaContribution(TimelineUpdate):

    def __init__(self, time, title, url):
        slug = str(filter(unicode.isalnum, url.replace('http://', '').replace('https://', ''))).lower()
        content = 'contributed to wikipedia at [%s](%s)' % (title, url)
        TimelineUpdate.__init__(self, slug, title, url, time, content)
        self.actions.append(('show changes', url))


def add_wikipedia_actions_to_timeline(options, content_dir='./content/timeline/'):
    config = Configuration('wikipedia.config')
    assert config['lang'], 'lang must be set in wikipedia.config'
    assert config['user'], 'user must be set in wikipedia.config'
    url = 'https://%(lang)s.wikipedia.org/w/api.php?action=feedcontributions&user=%(user)s&namespace=0&feedformat=atom' % config
    for entry in feedparser.parse(url).entries:
        time = datetime.datetime(entry.updated_parsed.tm_year, entry.updated_parsed.tm_mon, entry.updated_parsed.tm_mday, entry.updated_parsed.tm_hour, entry.updated_parsed.tm_min, entry.updated_parsed.tm_sec)
        title, link = entry.title, entry.link
        WikipediaContribution(time, title, link).save(content_dir)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s:%(message)s', level=logging.DEBUG)
    import os
    os.chdir('..')
    add_wikipedia_actions_to_timeline({}, '/tmp/')