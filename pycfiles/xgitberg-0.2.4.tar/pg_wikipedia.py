# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/pg_wikipedia.py
# Compiled at: 2016-03-15 10:09:17
from wikipedia import wikipedia
from wikipedia.exceptions import PageError, WikipediaException, DisambiguationError
import csv, requests, logging
_table = {}

def get_item_summary(wd_id, lang='en'):
    if wd_id is None:
        return
    else:
        try:
            r = requests.get(('https://www.wikidata.org/wiki/Special:EntityData/{}.json').format(wd_id))
        except:
            logging.warning(("couldn't get https://www.wikidata.org/wiki/Special:EntityData/{}.json").format(wd_id))
            return ''

        try:
            title = r.json()['entities'][wd_id]['sitelinks'][('{}wiki').format(lang)]['title']
            try:
                return wikipedia.summary(title)
            except (PageError, WikipediaException, DisambiguationError):
                logging.warning(("couldn't get wikipedia.summary({})").format(title))
                return ''

        except ValueError:
            return ''

        return


def get_links(wd_id):
    r = requests.get(('https://www.wikidata.org/wiki/Special:EntityData/{}.json').format(wd_id))
    try:
        sitelinks = r.json()['entities'][wd_id]['sitelinks'].values()
        return [ sitelink['url'] for sitelink in sitelinks ]
    except ValueError:
        return ''


def get_wd_id(pg_id):
    pg_id = str(pg_id)
    return _table.get(pg_id, None)


def get_pg_summary(pg_id):
    return get_item_summary(get_wd_id(pg_id))


def get_pg_links(pg_id):
    return get_links(get_wd_id(pg_id))


pg_wd_file = requests.get('https://raw.githubusercontent.com/gitenberg-dev/pg-wikipedia/master/pg-wd.csv')
csvreader = csv.reader(pg_wd_file.iter_lines(), delimiter=',', quotechar='"')
for pg_id, wd_id in csvreader:
    _table[pg_id] = wd_id