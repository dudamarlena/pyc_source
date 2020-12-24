# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/integrationdocs.py
# Compiled at: 2019-12-24 12:23:23
from __future__ import absolute_import
import os, sys, json, logging, time, sentry
BASE_URL = 'https://docs.sentry.io/_platforms/{}'
DOC_FOLDER = os.environ.get('INTEGRATION_DOC_FOLDER') or os.path.abspath(os.path.join(os.path.dirname(sentry.__file__), 'integration-docs'))
if sys.version_info[0] == 3:

    def iteritems(d, **kw):
        return iter(d.items(**kw))


    from urllib.request import urlopen
else:

    def iteritems(d, **kw):
        return d.iteritems(**kw)


    from urllib2 import urlopen
logger = logging.getLogger('sentry')

def echo(what):
    sys.stdout.write(what)
    sys.stdout.write('\n')
    sys.stdout.flush()


def dump_doc(path, data):
    fn = os.path.join(DOC_FOLDER, path + '.json')
    directory = os.path.dirname(fn)
    try:
        os.makedirs(directory)
    except OSError:
        pass

    with open(fn, 'wb') as (f):
        json.dump(data, f, indent=2)
        f.write('\n')


def load_doc(path):
    if '/' in path:
        return
    else:
        fn = os.path.join(DOC_FOLDER, path + '.json')
        try:
            with open(fn, 'rb') as (f):
                return json.load(f)
        except IOError:
            return

        return


def get_integration_id(platform_id, integration_id):
    if integration_id == '_self':
        return platform_id
    return ('{}-{}').format(platform_id, integration_id)


def urlopen_with_retries(url, timeout=5, retries=10):
    for i in range(retries):
        try:
            return urlopen(url, timeout=timeout)
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(i * 0.01)


def sync_docs(quiet=False):
    if not quiet:
        echo('syncing documentation (platform index)')
    body = urlopen_with_retries(BASE_URL.format('_index.json')).read().decode('utf-8')
    data = json.loads(body)
    platform_list = []
    for platform_id, integrations in iteritems(data['platforms']):
        platform_list.append({'id': platform_id, 
           'name': integrations['_self']['name'], 
           'integrations': [ {'id': get_integration_id(platform_id, i_id), 'name': i_data['name'], 'type': i_data['type'], 'link': i_data['doc_link']} for i_id, i_data in sorted(iteritems(integrations), key=lambda x: x[1]['name'])
                         ]})

    platform_list.sort(key=lambda x: x['name'])
    dump_doc('_platforms', {'platforms': platform_list})
    for platform_id, platform_data in iteritems(data['platforms']):
        for integration_id, integration in iteritems(platform_data):
            sync_integration_docs(platform_id, integration_id, integration['details'], quiet)


def sync_integration_docs(platform_id, integration_id, path, quiet=False):
    if not quiet:
        echo('  syncing documentation for %s.%s integration' % (platform_id, integration_id))
    data = json.load(urlopen_with_retries(BASE_URL.format(path)))
    key = get_integration_id(platform_id, integration_id)
    dump_doc(key, {'id': key, 'name': data['name'], 'html': data['body'], 'link': data['doc_link']})


def integration_doc_exists(integration_id):
    docs = os.listdir(DOC_FOLDER)
    filename = ('{}.json').format(integration_id)
    return filename in docs