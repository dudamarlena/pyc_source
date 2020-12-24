# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/utils.py
# Compiled at: 2015-04-28 15:32:14
import cStringIO, hashlib, logging, mimetypes, os, re, json
from urllib import urlopen, urlencode, urlretrieve
import urllib2
from lxml import etree
import pylast
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from django.conf import settings

def _wikipedia(instance):
    from music.models import TrackContributor, Track, Album
    if isinstance(instance, TrackContributor):
        search = instance.title + ' artist band'
    else:
        if isinstance(instance, Track):
            contributors = instance.get_primary_contributors()
            if contributors:
                search = contributors[0].title + ' artist band'
            else:
                search = instance.title + ' song'
        elif isinstance(instance, Album):
            search = instance.title + ' album'
        else:
            return
        url = 'http://en.wikipedia.org/w/api.php'
        headers = {'User-Agent': 'Jmbo Show HTTP Request'}
        params = {'action': 'query', 
           'list': 'search', 
           'srsearch': unicode(search).encode('utf-8'), 
           'srlimit': 1, 
           'format': 'json'}
        request = urllib2.Request(url, urlencode(params), headers)
        response = urllib2.urlopen(request)
        data = response.read()
        struct = json.loads(data)
        try:
            title = struct['query']['search'][0]['title']
        except (KeyError, IndexError):
            return

    params = {'action': 'query', 'prop': 'revisions', 
       'titles': unicode(title).encode('utf-8'), 
       'rvprop': 'content', 
       'rvsection': 0, 
       'format': 'xml'}
    request = urllib2.Request(url, urlencode(params), headers)
    response = urllib2.urlopen(request)
    data = response.read()
    m = re.search('(Cover|image)[\\s=]*([^\\|]*)', data, re.M | re.I | re.DOTALL)
    if m:
        filename = m.group(2).strip()
        params = {'action': 'query', 
           'prop': 'imageinfo', 
           'titles': 'File:%s' % filename, 
           'iiprop': 'url', 
           'format': 'xml'}
        request = urllib2.Request(url, urlencode(params), headers)
        response = urllib2.urlopen(request)
        data = response.read()
        xml = etree.fromstring(data)
        el = xml.find('.//ii')
        if el is not None:
            url_attr = el.get('url')
            if url_attr:
                tempfile = urlretrieve(url_attr)
                instance.image.save(filename, File(open(tempfile[0])))
    return


def wikipedia(instance):
    try:
        _wikipedia(instance)
    except Exception as e:
        logging.warn('_wikipedia - title %s exception %s' % (
         instance.title, e))


def _lastfm(instance):
    di = getattr(settings, 'JMBO_MUSIC', {})
    try:
        api_key = settings.JMBO_MUSIC['lastfm_api_key']
        api_secret = settings.JMBO_MUSIC['lastfm_api_secret']
    except (AttributeError, KeyError):
        raise RuntimeError('Settings is not configured properly')

    network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
    from music.models import TrackContributor, Track, Album
    if isinstance(instance, TrackContributor):
        try:
            obj = network.get_artist(instance.title)
        except pylast.WSError:
            return

    else:
        if isinstance(instance, Track):
            contributors = instance.get_primary_contributors()
            if contributors:
                try:
                    obj = network.get_artist(contributors[0].title)
                except pylast.WSError:
                    return

            else:
                return
        elif isinstance(instance, Album):
            tracks = instance.track_set.all()
            contributors = None
            if tracks:
                contributors = tracks[0].get_primary_contributors()
            if contributors:
                artist = contributors[0].title
            else:
                artist = None
            try:
                obj = network.get_album(artist, instance.title)
            except pylast.WSError:
                return

        else:
            return
        try:
            url = obj.get_cover_image()
        except pylast.WSError:
            return

    if url:
        filename = url.split('/')[(-1)]
        tempfile = urlretrieve(url)
        instance.image.save(filename, File(open(tempfile[0])))
    return


def lastfm(instance):
    try:
        _lastfm(instance)
    except Exception as e:
        logging.warn('_lastfm - title %s exception %s' % (
         instance.title, e))


def scrape_image(instance):
    di = getattr(settings, 'JMBO_MUSIC', {})
    scrapers = di.get('scrapers', ('lastfm', 'wikipedia'))
    for scraper in scrapers:
        globals()[scraper](instance)
        if instance.image:
            break