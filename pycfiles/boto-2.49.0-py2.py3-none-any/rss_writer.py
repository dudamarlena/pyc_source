# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/rss_writer.py
# Compiled at: 2012-08-16 08:14:56
__doc__ = '\nSimple RSS Writer that uses WebHelpers Rss201rev2Feed\n\nExample usage:\n\ndocs = [\n    {\n        \'title\': \'doc 1\', \n        \'url\': \'http://www.test.com\',\n        \'description\': \'some description\',\n    },\n    {\n        \'title\': \'doc 2\', \n        \'url\': \'http://www.abc.com\',\n        \'description\': \'another description\',\n    }\n    ]\n    \nbotnee.rss_writer.write_string(docs)\n\nResult:\n\'<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"><channel><title>Botnee Feed</title><link>http://www.bmjgroup.com</link><description>A sample feed, showing how to make and add entries</description><language>en</language><lastBuildDate>Thu, 01 Mar 2012 14:32:49 -0000</lastBuildDate><item><title>doc 1</title><link>http://www.test.com</link><description>Testing.</description></item><item><title>doc 2</title><link>http://www.abc.com</link><description>Testing.</description></item></channel></rss>\'\n'
from django.utils.feedgenerator import Rss201rev2Feed as RssFeed
from webhelpers.feedgenerator import rfc3339_date as rfc_date
from time import time
import datetime, hashlib
from botnee.standard_document import StandardDocument
from botnee import debug
import botnee_config, logging
rss_logger = logging.getLogger(__name__)
BASE_URL = 'http://group.bmj.com/'

def write_feed(summary, feed_title='Botnee Feed', feed_description='A Sample Feed', feed_url=BASE_URL, feed_seed='', verbose=False):
    """
    Returns feed as string
    """
    with debug.Timer(None, None, verbose, rss_logger):
        feed = BotneeFeed(summary, feed_title, feed_description, feed_url, feed_seed, verbose)
        try:
            feed_string = feed.writeString('utf-8')
        except Exception, e:
            errors.RssWriterWarning(e.__repr__(), rss_logger)
            feed_string = ''

        return feed_string
    return


class BotneeFeed(RssFeed):
    """
    Subclass of generic feed with custom properties for botnee
    """

    def __init__(self, summary, feed_title='Botnee Feed', feed_description='A Sample Feed', feed_url='http://www.bmjgroup.com', feed_seed='', verbose=False):
        feed_guid = 'bmj:botnee:' + hashlib.md5(str(time())).hexdigest()
        lastBuildDate = rfc_date(datetime.datetime.now()).decode('utf-8')
        if botnee_config.DEBUG:
            feed_description += '\n\n' + feed_seed
        RssFeed.__init__(self, feed_title, feed_url, feed_description, feed_url=feed_url, feed_guid=feed_guid, lastBuildDate=lastBuildDate)
        for doc in summary:
            self.add_standard_doc(doc, verbose)

    def add_standard_doc(self, doc, verbose=False):
        """
        Creates atom from StandardDocument
        """
        if type(doc) is not StandardDocument:
            raise TypeError('Expected StandardDocument, got %s' % str(type(doc)))
        unique_id = doc['guid']
        title = doc['title']
        link = doc['url']
        pubdate = doc['publication-date']
        source = doc['publication']
        description = doc['extra']
        if type(pubdate) is not datetime.datetime:
            raise TypeError('Expected datetime, got %s' % str(type(pubdate)))
        try:
            categories_cust = [
             (
              'journal_section', doc['journal_section'])]
        except KeyError:
            categories_cust = []
            msg = '%s: No journal section' % unique_id
            debug.print_verbose(msg, verbose, rss_logger)

        self.add_item(title=title, link=link, pubdate=pubdate, unique_id=unique_id, categories_cust=categories_cust, source=source, description=description)

    def add_item_elements(self, handler, item):
        RssFeed.add_item_elements(self, handler, item)
        if item['source'] is not None:
            try:
                handler.addQuickElement('source', item['source'], {'url': BASE_URL})
            except Exception, e:
                errors.RssWriterWarning(e.__repr__(), rss_logger)

        if item['categories_cust'] is not None:
            try:
                for cat in item['categories_cust']:
                    handler.addQuickElement('category', cat[1], {'domain': cat[0]})

            except Exception, e:
                errors.RssWriterWarning(e.__repr__(), rss_logger)

        return