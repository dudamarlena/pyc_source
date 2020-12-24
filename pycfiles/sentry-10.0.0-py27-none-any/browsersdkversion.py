# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/loader/browsersdkversion.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import os, re, logging, json, six
from pkg_resources import parse_version
from functools32 import lru_cache
import sentry
from django.conf import settings
logger = logging.getLogger('sentry')
_version_regexp = re.compile('^\\d+\\.\\d+\\.\\d+$')
LOADER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(sentry.__file__), 'loader'))

@lru_cache(maxsize=10)
def load_registry(path):
    if '/' in path:
        return
    else:
        fn = os.path.join(LOADER_FOLDER, path + '.json')
        try:
            with open(fn, 'rb') as (f):
                return json.load(f)
        except IOError:
            return

        return


def get_highest_browser_sdk_version(versions):
    full_versions = filter(lambda x: _version_regexp.match(x), versions)
    if full_versions:
        return six.binary_type(max(map(parse_version, full_versions)))
    return settings.JS_SDK_LOADER_SDK_VERSION


def get_browser_sdk_version_versions():
    return [
     'latest', '5.x', '4.x']


def get_browser_sdk_version_choices():
    rv = []
    for version in get_browser_sdk_version_versions():
        rv.append((version, version))

    return tuple(rv)


def load_version_from_file():
    data = load_registry('_registry')
    if data:
        return data.get('versions', [])
    return []


def get_highest_selected_browser_sdk_version(selected_version):
    versions = load_version_from_file()
    if selected_version == 'latest':
        return get_highest_browser_sdk_version(versions)
    return get_highest_browser_sdk_version(filter(lambda x: x.startswith(selected_version[0]), versions))


def get_browser_sdk_version(project_key):
    selected_version = get_selected_browser_sdk_version(project_key)
    try:
        return get_highest_selected_browser_sdk_version(selected_version)
    except BaseException:
        logger.error('error ocurred while trying to read js sdk information from the registry')
        return settings.JS_SDK_LOADER_SDK_VERSION


def get_selected_browser_sdk_version(project_key):
    return project_key.data.get('browserSdkVersion') or get_default_sdk_version_for_project(project_key.project)


def get_default_sdk_version_for_project(project):
    return project.get_option('sentry:default_loader_version')