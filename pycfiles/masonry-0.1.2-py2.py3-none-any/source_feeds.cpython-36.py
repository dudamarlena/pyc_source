# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cmusselle/Mango/Workspace/rss-miner/package/src/rss_miner/source_feeds.py
# Compiled at: 2017-05-14 11:27:36
# Size of source mod 2**32: 3751 bytes
import feedparser
from tinydb import Query
import time

def max_entry_date(feed):
    """Return the max published time in all entries of a feed"""
    entry_pub_dates = tuple(e.get('published_parsed') for e in feed.entries if 'published_parsed' in e)
    if entry_pub_dates:
        return max(entry_pub_dates)


def fetch_new_entries(source, db):
    """ Returns a list of new entries from a feed

    Looks up metadata and does not return entries already seen

    Parameters
    ----------
    source: dict
        keys name and url for the data source
    db: TinyDB
        Database for the metadata

    Returns
    -------
    list:
        Entries that have not yet been seen (may be empty)
    """
    name = source['name']
    url = source['url']
    src = Query()
    result = db.table('meta').get(src.name == name)
    if not result:
        new_feed = feedparser.parse(url)
        updated, updated_parsed = get_last_updated_times(new_feed)
        data = {'name':name, 
         'updated':updated, 
         'updated_parsed':updated_parsed, 
         'title':new_feed.feed.title, 
         'subtitle':new_feed.feed.subtitle, 
         'url':url, 
         'max_entry_date':max_entry_date(new_feed), 
         'etag':new_feed.get('etag'), 
         'modified':new_feed.get('modified')}
        db.table('meta').insert(data)
        entries = new_feed.entries
    if result:
        etag = result.get('etag', None)
        modified = result.get('modified', None)
        new_feed = feedparser.parse(url, etag=etag, modified=modified)
        entries = []
        if new_feed.entries:
            prev_max_date = result['max_entry_date']
            entries = [e for e in new_feed.entries if e.get('published_parsed') > prev_max_date]
            n_filtered = len(new_feed.entries) - len(entries)
            print('{} articles filtered out as already processed'.format(n_filtered))
            print('{} new articles'.format(len(entries)))
            if entries:
                updated, updated_parsed = get_last_updated_times(new_feed)
                data = {'name':name, 
                 'updated':updated, 
                 'updated_parsed':updated_parsed, 
                 'title':new_feed.feed.title, 
                 'subtitle':new_feed.feed.subtitle, 
                 'url':url, 
                 'max_entry_date':max_entry_date(new_feed), 
                 'etag':new_feed.get('etag'), 
                 'modified':new_feed.get('modified')}
                db.table('meta').update(data, eids=[result.eid])
    return entries


def get_last_updated_times(feed):
    if not feed.feed.get('updated'):
        updated_parsed = max_entry_date(feed)
        updated = time.strftime('%a, %d %b %Y %H:%M:%S %Z')
    else:
        updated_parsed = feed.feed.updated_parsed
        updated = feed.feed.updated
    return (updated, updated_parsed)