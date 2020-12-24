# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jfurr/django-mongolog/mongolog/management/commands/analog.py
# Compiled at: 2019-01-13 19:05:20
from __future__ import print_function
import logging, logging.config, json, pymongo
pymongo_version = int(pymongo.version.split('.')[0])
if pymongo_version >= 3:
    from pymongo.collection import ReturnDocument
from mongolog.models import get_mongolog_handler
from django.core.management.base import BaseCommand
logger = logging.getLogger('console')

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.prev_object_id = None
        return

    def add_arguments(self, parser):
        parser.add_argument('-l', '--limit', default=10, type=int, action='store', dest='limit', help='Limit Results')
        parser.add_argument('-t', '--tail', default=False, action='store_true', dest='tail', help='Tail the log file.  By default it will limit to 10 results.  Use --limit to change')
        parser.add_argument('-q', '--query', default=None, type=str, action='store', dest='query', help='Pass in a search query to mongo.')
        return

    def print_results(self, results):
        try:
            results = list(results['result'])
            results.reverse()
        except TypeError:
            pass

        for r in results:
            level = r.get('level', None)
            if level == 'INFO':
                logger.info(r)
            elif level == 'WARNING':
                logger.warn(r)
            elif level == 'ERROR':
                logger.error(r)
            elif level == 'DEBUG':
                logger.debug(r)
            elif level == 'CRITICAL':
                logger.critical(r)
            elif level == 'MONGOLOG-INTERNAL' or level is None:
                pass
            else:
                raise Exception('level(%s) not found' % level)

        return

    def fetch_results(self, options):
        query = options['query'] if options['query'] else {}
        proj = {'_id': 1, 'level': 1, 'msg': 1}
        limit = options['limit']
        return self.collection.aggregate([{'$match': query}, {'$project': proj}, {'$sort': {'created': pymongo.DESCENDING}}, {'$limit': limit}])

    def tail(self, options):
        initial = self.fetch_results(options)
        self.print_results(initial)
        raise NotImplementedError('--tail not finshed')

    def handle(self, *args, **options):
        if options['query']:
            options['query'] = json.loads(options['query'])
        handler = get_mongolog_handler('simple')
        self.collection = handler.get_collection()
        if options['tail']:
            self.tail(options)
        else:
            results = self.fetch_results(options)
            self.print_results(results)