# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/opps/feedcrawler/management/commands/process_feeds.py
# Compiled at: 2014-09-18 10:30:30
"""
This command polls all of the Feeds and inserts any new entries found.
"""
from optparse import make_option
from django.core.management.base import BaseCommand
from opps.feedcrawler.models import Feed
import logging
logger = logging.getLogger()
from django.db import transaction

class Command(BaseCommand):
    args = 'none'
    help = 'run the feed processor for every published feed.'
    option_list = BaseCommand.option_list + (
     make_option('--verbose', action='store_true', dest='verbose', default=False, help='Print progress on command line'),
     make_option('--feed', action='store_true', dest='feed', default=False, help='Process only specified feed'))

    def handle(self, *args, **options):
        """
        Read through all the feeds looking for new entries.
        """
        verbose = options.get('verbose')
        feed_slug = options.get('feed')
        if feed_slug:
            feeds = Feed.objects.filter(slug=feed_slug)
        else:
            feeds = Feed.objects.filter(published=True)
        num_feeds = feeds.count()
        if verbose:
            print '%d feeds to process' % num_feeds
        for i, feed in enumerate(feeds):
            try:
                with transaction.commit_manually():
                    if verbose:
                        print '(%d/%d) Processing Feed %s' % (
                         i + 1, num_feeds, feed.title)
                    processor = feed.get_processor(verbose)
                    if processor:
                        if verbose:
                            print 'Processing: %s' % processor.__class__
                        try:
                            processor.process()
                        except Exception as e:
                            if verbose:
                                print str(e)

                    transaction.commit()
            except Exception as e:
                msg = ('{f.title} - {msg}').format(f=feed, msg=str(e))
                logger.warning(msg)

        logger.info('Feedcrawler process_feeds completed successfully')