# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/upodder/upodder.py
# Compiled at: 2017-08-18 02:13:21
from __future__ import print_function
import feedparser, listparser, time, hashlib, os, sys
from os.path import expanduser
import logging, re, requests, argparse, shutil
from datetime import datetime as dt
from sqlobject import SQLObject, sqlite, DateTimeCol, UnicodeCol
from tqdm import tqdm
try:
    input = raw_input
except NameError:
    pass

parser = argparse.ArgumentParser(description='Download podcasts via the command line.')
parser.add_argument('--no-download', action='store_true', help="Don't download any files. Just mark as read.")
parser.add_argument('--podcastdir', '-p', default='~/Downloads/podcasts', help='Folder to download podcast files to.')
parser.add_argument('--basedir', '-b', default='~/.upodder', help='Folder to store subscriptions and seen database.')
parser.add_argument('--oldness', '-o', default=30, type=int, help='Skip entries older than X days.')
parser.add_argument('--mark-seen', action='store_true', help='Just mark all entries as seen and exit.')
parser.add_argument('--import-opml', '-i', dest='opmlpath', help='Import feeds from an OPML file.')
parser.add_argument('--quiet', help='Only output errors.', action='store_true')
args = parser.parse_args()
YES = [
 1, '1', 'on', 'yes', 'Yes', 'YES', 'y', 'Y', 'true', 'True', 'TRUE', 't', 'T']
CONFIGCOMMENT = ['#', ';', '$', ':', '"', "'"]
BADFNCHARS = re.compile('[^\\w]+')
TEMPDIR = '/tmp/upodder'
FILENAME = '{entry_title}.{filename_extension}'
if args.quiet:
    l = logging.Logger('upodder', logging.ERROR)
else:
    l = logging.Logger('upodder', logging.DEBUG)
stderrHandler = logging.StreamHandler()
l.addHandler(stderrHandler)
FILE_TYPES = {'audio/mpeg': 'mp3', 
   'audio/x-m4a': 'm4a', 
   'video/x-m4v': 'm4v', 
   'audio/x-opus': 'opus', 
   'audio/x-ogg': 'ogg', 
   'audio/aac': 'aac', 
   'audio/mp4': 'm4a', 
   'audio/mp3': 'mp3'}

class SeenEntry(SQLObject):
    """Represents a single feed item, seen before. Used to keep track of download status."""
    hashed = UnicodeCol()
    pub_date = DateTimeCol()


class EntryProcessor(object):
    """Processes single feed entry"""

    def __init__(self, entry, feed):
        self.hashed = hashlib.sha1(entry['title'].encode('ascii', 'ignore')).hexdigest()
        self.pub_date = dt.fromtimestamp(time.mktime(entry.published_parsed))
        if args.mark_seen:
            SeenEntry(pub_date=self.pub_date, hashed=self.hashed)
            l.debug('Marking as seen: %s' % entry['title'])
            return
        if SeenEntry.select(SeenEntry.q.hashed == self.hashed).count() > 0:
            l.debug('Already seen: %s' % entry['title'])
            return
        if (dt.now() - self.pub_date).days > args.oldness:
            l.debug('Too old for us: %s' % entry['title'])
            return
        for enclosure in filter(lambda x: x.get('type') in FILE_TYPES.keys(), entry.get('enclosures', [])):
            entry['type'] = enclosure.get('type')
            if self._download_enclosure(enclosure, entry, feed, args.no_download):
                SeenEntry(pub_date=self.pub_date, hashed=self.hashed)
            break

    def _download_enclosure(self, enclosure, entry, feed, no_download=False):
        """Performs downloading of specified file. Returns True on success and False in other case"""
        downloadto = TEMPDIR + os.sep + self.hashed
        if no_download:
            l.debug('Would download %s from %s' % (entry['title'], enclosure['href']))
            return True
        try:
            if not os.path.exists(os.path.dirname(downloadto)):
                os.makedirs(os.path.dirname(downloadto))
            l.debug('Downloading %s from %s' % (entry['title'], enclosure['href']))
            r = requests.get(enclosure['href'], stream=True, timeout=25)
            with open(downloadto, 'wb') as (f):
                if 'content-length' in r.headers:
                    total_length = int(r.headers['content-length'])
                    with tqdm(total=total_length, unit='B', unit_scale=True, ncols=90) as (pbar):
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                            if chunk:
                                pbar.update(len(chunk))

                else:
                    for chunk in r.iter_content(1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()

        except KeyboardInterrupt:
            l.info('Download aborted by Ctrl+c')
            try:
                user_wish = input('Do you like to mark item as read? (y/n) or quit? (Ctrl+c): ')
                if user_wish in YES:
                    return True
                return False
            except KeyboardInterrupt:
                print('\nQuitting')
                sys.exit()

        moveto = expanduser(args.podcastdir) + os.sep + self._generate_filename(entry, feed)
        l.debug('Moving {%s} to {%s}' % (downloadto, moveto))
        if not os.path.exists(os.path.dirname(moveto)):
            os.makedirs(os.path.dirname(moveto))
        shutil.move(downloadto, moveto)
        return True

    def _generate_filename(self, entry, feed):
        """Generates file name for this enclosure based on config settins
           Added filename_extension dict mapping to handle different file types."""
        year, month, day, hour, minute, second, weekday, yearday, leap = time.localtime()
        subst = {'today': '%i-%02i-%02i' % (year, month, day), 
           'entry_date': self.pub_date.date().isoformat(), 
           'id': self.hashed, 
           'entry_title': re.sub(BADFNCHARS, '_', entry.get('title')), 
           'feed_href': re.sub(BADFNCHARS, '_', feed.href.split('://')[(-1)]), 
           'feed_title': re.sub(BADFNCHARS, '_', feed.feed.get('title', feed.href)), 
           'filename_extension': FILE_TYPES.get(entry.get('type'))}
        return FILENAME.format(**subst)


def process_feed(url):
    l.info('Downloading feed: %s' % url)
    feed = feedparser.parse(url)
    if feed.bozo and isinstance(feed.bozo_exception, (
     type(feedparser.NonXMLContentType), type(feedparser.CharacterEncodingOverride))):
        l.error('Erroneous feed URL: %s (%s)' % (url, type(feed.bozo_exception)))
        return
    if 'title' not in feed.feed:
        l.error('Erroneous feed URL: %s' % url)
        return
    l.info('Parsing feed: %s' % feed.feed.title)
    feed.entries.reverse()
    for entry in feed.entries:
        EntryProcessor(entry, feed)


def import_opml(subscriptions, opml):
    """Import a list of subscriptions from an OPML file."""
    subscribed_feeds = []
    imported_feeds = listparser.parse(opml)
    with open(subscriptions, 'r') as (f):
        for line in f:
            feed = line.strip()
            if feed.startswith('#') or len(feed) == 0:
                continue
            subscribed_feeds.append(feed)

    with open(subscriptions, 'a') as (f):
        for feed in imported_feeds.feeds:
            if feed.url not in subscribed_feeds:
                print('Importing ' + feed.title + '...')
                subscribed_feeds.append(feed.url)
                f.write(feed.url + '\n')

    sys.exit()


def init():
    if not os.path.exists(expanduser(args.basedir)):
        l.info('Creating base dir %s' % args.basedir)
        os.makedirs(expanduser(args.basedir))
    subscriptions = expanduser(args.basedir) + os.sep + 'subscriptions'
    if not os.path.exists(subscriptions):
        l.info('Creating empty subscriptions file %s' % subscriptions)
        open(subscriptions, 'a').write('# Add your RSS/ATOM subscriptions here.\n\n')
    if args.opmlpath:
        import_opml(subscriptions, args.opmlpath)
    SeenEntry._connection = sqlite.builder()(expanduser(args.basedir + os.sep + 'seen.sqlite'), debug=False)
    SeenEntry.createTable(ifNotExists=True)


def main():
    init()
    for url in map(lambda x: x.strip(), open(expanduser(args.basedir) + os.sep + 'subscriptions')):
        if url and url[0] not in CONFIGCOMMENT:
            process_feed(url)

    l.info('Done updating feeds.')


if __name__ == '__main__':
    main()