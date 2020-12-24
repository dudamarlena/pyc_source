# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skins/skin.py
# Compiled at: 2010-03-20 20:08:48
"""Provides template skinning abilities for templates.

:Authors:
    - Bruce Kroeze
"""
__docformat__ = 'restructuredtext'
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from glob import glob
from skins.skin_settings import get_skin_setting
from threaded_multihost import threadlocals
from threaded_multihost.utils import current_media_url
import logging, os, simplejson, utils
log = logging.getLogger('skins.skin')
_CACHE = {}

class Skin(object):

    def __init__(self, path):
        self.path = path
        self.key = self.path.split(os.path.sep)[(-1)]
        self.info = self._skin_info()
        self.name = self.info['name']
        self.version = self.info.get('version', 1)
        self.author = self.info.get('author', 'Unknown')

    def _skin_info(self):
        config = os.path.join(self.path, 'CONFIG.json')
        skindata = {}
        if utils.is_file(config):
            cf = open(config, 'r')
            data = cf.read()
            try:
                skindata = simplejson.loads(data)
            except Exception, e:
                log.debug('%s\n%s', e, data)

        name = skindata.get('name', None)
        if not name:
            name = self.key
            skindata['name'] = name
        return skindata

    def _media_url(self):
        return utils.url_join(current_media_url(), 'skins', self.key, '/')

    media_url = property(fget=_media_url)

    def __cmp__(self, other):
        return cmp((self.name, self.version), (other.name, other.version))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


def active_skin():
    key = threadlocals.get_thread_variable('skin', None)
    if not key:
        site = Site.objects.get_current()
        q = site.skin.all()
        if q.count() > 0:
            key = q[0].name
            log.debug('skin for %s is %s', site.domain, key)
    if not key:
        key = get_skin_setting('DEFAULT_SKIN')
    keys = get_skin_keys()
    if key not in keys:
        if len(keys) > 0:
            log.warn("Cannot find active skin '%s' in skin list, using default skin '%s'", key, keys[0])
            key = keys[0]
        else:
            log.fatal('No Skins found - cannot return any default skin.')
    remember_skin(key)
    return get_skin(key)


def get_skin(path):
    global _CACHE
    load_skins()
    return _CACHE[path]


def get_skin_choices():
    load_skins()
    choices = _CACHE.values()
    choices.sort()
    return [ (skin.key, skin.name) for skin in choices ]


def get_skin_keys():
    load_skins()
    choices = _CACHE.values()
    choices.sort()
    return [ skin.key for skin in choices ]


def load_skins():
    if not len(_CACHE) > 0:
        skindirs = get_skin_setting('SKIN_DIRS')
        log.debug('Loading skins from %s', skindirs)
        skindirs = utils.get_flat_list(skindirs)
        skindirs = [ os.path.join(s, '*') for s in skindirs if s ]
        for skindir in skindirs:
            for path in glob(skindir):
                if utils.is_dir(path):
                    skin = Skin(path)
                    log.debug('adding %s' % skin.key)
                    _CACHE[skin.key] = skin

        if len(_CACHE) == 0:
            log.error('No skins found in %s', skindirs)
            raise ImproperlyConfigured('No skins loaded - noting found in skin directories, searched: %s', ('\n').join(skindirs))
        log.debug('Loaded skins')


def remember_skin(key):
    threadlocals.set_thread_variable('skin', key)