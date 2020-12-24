# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/distutils/commands/build_js_sdk_registry.py
# Compiled at: 2019-11-01 16:39:36
from __future__ import absolute_import
import os, sys, json
from distutils import log
import sentry
JS_SDK_REGISTRY_URL = 'https://release-registry.services.sentry.io/sdks/sentry.javascript.browser/versions'
LOADER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(sentry.__file__), 'loader'))
if sys.version_info[0] == 3:

    def iteritems(d, **kw):
        return iter(d.items(**kw))


    from urllib.request import urlopen
else:

    def iteritems(d, **kw):
        return d.iteritems(**kw)


    from urllib2 import urlopen

def dump_registry(path, data):
    fn = os.path.join(LOADER_FOLDER, path + '.json')
    directory = os.path.dirname(fn)
    try:
        os.makedirs(directory)
    except OSError:
        pass

    with open(fn, 'wb') as (f):
        json.dump(data, f, indent=2)
        f.write('\n')


def sync_registry():
    body = urlopen(JS_SDK_REGISTRY_URL).read().decode('utf-8')
    data = json.loads(body)
    dump_registry('_registry', data)


from .base import BaseBuildCommand

class BuildJsSdkRegistryCommand(BaseBuildCommand):
    description = 'build js sdk registry'

    def run(self):
        log.info('downloading js sdk information from the release registry')
        try:
            sync_registry()
        except BaseException:
            log.error('error occurred while trying to fetch js sdk information from the registry')