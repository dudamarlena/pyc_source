# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wok_hooks/hook_diaspora.py
# Compiled at: 2014-10-09 05:50:09
import logging
from wok_hooks.misc import Configuration as _Configuration
from activitystreams import Activity as PostActivity, Object as NoteObject
from activitystreams.atom import make_activities_from_feed
import urllib2, xml.etree.ElementTree, html2text, os
from wok_hooks.timeline import Post as TimelineUpdate

class Configuration(_Configuration):
    DEFAULTS = {'pod': '', 'user': ''}

    def __init__(self, path, **kwargs):
        _Configuration.__init__(self, path, **kwargs)
        for key, value in Configuration.DEFAULTS.items():
            if key not in self:
                self[key] = value
                self.save()


class DiasporaNote(TimelineUpdate):
    TITLE_CHAR_BLACKLIST = [
     '[', '!', '*', ':']

    def __init__(self, base_object, time, pod):
        assert isinstance(base_object, NoteObject)
        slug = base_object.id.replace('https://%s/' % pod, pod + '-').replace('/', '-').replace('_', '-').replace('.', '-')
        title = base_object.name
        for char in DiasporaNote.TITLE_CHAR_BLACKLIST:
            title = title.replace(char, '')

        url = base_object.url
        content = base_object.content
        content = html2text.html2text(content)
        TimelineUpdate.__init__(self, slug, title, url, time, content)
        self.actions.append(('show diaspora', url))


def add_diaspora_posts_to_timeline(options, content_dir='./content/timeline/'):
    config = Configuration('diaspora.config')
    assert config['pod'], 'pod must be set in diaspora.config'
    url = '%spublic/%s.atom' % ('https://%s/' % config['pod'], config['user'])
    logging.info('read %s', url)
    try:
        response = urllib2.urlopen(url)
        contents = response.read()
        xml_tree = xml.etree.ElementTree.fromstring(contents)
        xml_tree.getroot = lambda : xml_tree
        activities = make_activities_from_feed(xml_tree)
        for activity in activities:
            try:
                if isinstance(activity, PostActivity):
                    if isinstance(activity.object, NoteObject):
                        note = DiasporaNote(activity.object, activity.time, config['pod'])
                        note.save(content_dir)
                    else:
                        logging.debug('unexpected post object')
                else:
                    logging.debug('unknwon diaspora activity verb %s' % activity.verb)
            except Exception as ex:
                print ex

    except urllib2.HTTPError as ex:
        logging.info(ex)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s:%(message)s', level=logging.DEBUG)
    os.chdir('..')
    add_diaspora_posts_to_timeline({}, '/tmp/')