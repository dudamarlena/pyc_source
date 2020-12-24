# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eyefi/actions.py
# Compiled at: 2012-02-25 20:09:43
import os
from twisted.python import log
from twisted.internet import utils
from twisted.internet.defer import DeferredList
from eyefi.maclog import eyefi_parse, photo_macs
from eyefi.google_loc import google_loc
from eyefi.exif_gps import write_gps
from eyefi.twisted_flickrapi import TwistedFlickrAPI
import pyexiv2
assert pyexiv2.version_info[1] >= 2, 'need at least pyexiv 0.2.2'

class Action(object):
    name = 'action_name'

    def __init__(self, cfg, card):
        pass

    @classmethod
    def active_on_card(cls, card):
        return bool(card.get(cls.name, False))

    def handle_photo(self, card, files):
        pass

    def __call__(self, args):
        return self.handle_photo(*args)


_actions = []

def register_action(action):
    _actions.append(action)
    return action


def build_actions(cfg, cards):
    actions = {}
    for macaddress, card in cards.items():
        h = []
        for action in _actions:
            if action.active_on_card(card):
                h.append(action(cfg, card))

        actions[macaddress] = h

    return actions


@register_action
class ExtractPreview(Action):
    name = 'extract_preview'

    def handle_photo(self, card, files):
        for file in files[:]:
            base, ext = os.path.splitext(file)
            if ext.lower() in ('.nef', ):
                i = pyexiv2.metadata.ImageMetadata(file)
                i.read()
                p = i.previews[(-1)]
                p.write_to_file(str(base))
                j = pyexiv2.metadata.ImageMetadata(str(base) + p.extension)
                j.read()
                i.copy(j, exif=True, iptc=True, xmp=True, comment=True)
                j.write()
                files.append(str(base) + p.extension)
                log.msg('wrote preview', base, p.extension)

        return (
         card, files)


@register_action
class Geotag(Action):
    name = 'geotag'

    def handle_photo(self, card, files):
        logname = [ f for f in files if f.lower().endswith('.log') ][0]
        photoname = [ f for f in files if f is not log ][0]
        dir, name = os.path.split(photoname)
        data = list(eyefi_parse(logname))
        for photos, aps in data[::-1]:
            if name in photos:
                macs = photo_macs(photos[name], aps)
                loc = google_loc(wifi_towers=macs)
                loc.addCallback(self._write_loc, photoname, sidecar=card['geotag_sidecar'], xmp=card['geotag_xmp'])
                loc.addCallback(log.msg, 'geotagged')
                if card['geotag_delete_log']:
                    loc.addCallback(lambda _: os.remove(logname))
                    files.remove(logname)
                loc.addCallback(lambda _: (card, files))
                return loc

        return (
         card, files)

    @staticmethod
    def _write_loc(loc, photo, sidecar=True, xmp=False):
        if sidecar or photo.lower().endswith('.jpg'):
            loc = loc['location']
            write_gps(photo, loc['latitude'], loc['longitude'], loc.get('altitude', None), 'WGS-84', loc.get('accuracy', None), sidecar, xmp)
        return (
         loc, photo)


@register_action
class Geeqie(Action):
    name = 'geeqie'

    def handle_photo(self, card, files):
        d = utils.getProcessValue('/usr/bin/geeqie', [
         '--remote', str(files[0])], os.environ)
        d.addBoth(lambda _: (card, files))
        return d


@register_action
class Flickr(Action):
    name = 'flickr'

    def __init__(self, cfg, card):
        key, secret = cfg.get('__main__', 'flickr_key').split(':')
        self.flickr = TwistedFlickrAPI(key, secret)
        self.flickr.authenticate_console('write').addCallback(log.msg, 'got flickr token')

    def handle_photo(self, card, files):
        ds = []
        for file in files:
            if os.path.splitext(file)[1].lower() in ('.jpg', ):
                ds.append(self.flickr.upload(str(file), is_public=card['flickr_public'] and '1' or '0').addCallback(log.msg, 'upload to flickr'))

        d = DeferredList(ds, fireOnOneErrback=1)
        d.addCallback(lambda _: (card, files))
        return d


@register_action
class Run(Action):
    name = 'run'

    def handle_photo(self, card, files):
        d = utils.getProcessOutput(card['run'], files, os.environ)
        d.addCallback(log.msg)
        d.addCallback(lambda _: (card, files))
        return d