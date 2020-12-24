# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/core/novel_search.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2746 bytes
"""
To search for novels in selected sources
"""
import os, logging
from concurrent import futures
from slugify import slugify
from progress.bar import IncrementalBar
from ..sources import crawler_list
logger = logging.getLogger('SEARCH_NOVEL')

def get_search_result(user_input, link):
    try:
        crawler = crawler_list[link]
        instance = crawler()
        instance.home_url = link.strip('/')
        results = instance.search_novel(user_input)
        logger.debug(results)
        logger.info('%d results from %s', len(results), link)
        return results
    except Exception:
        import traceback
        logger.debug(traceback.format_exc())

    return []


def process_results(results):
    combined = dict()
    for result in results:
        key = slugify(result['title'])
        if len(key) <= 1:
            continue
        else:
            if key not in combined:
                combined[key] = []
        combined[key].append(result)

    processed = []
    for key, value in combined.items():
        value.sort(key=(lambda x: x['url']))
        processed.append({'id':key, 
         'title':value[0]['title'], 
         'novels':value})

    processed.sort(key=(lambda x: -len(x['novels'])))
    return processed[:15]


def search_novels(app):
    executor = futures.ThreadPoolExecutor(10)
    checked = {}
    futures_to_check = {}
    for link in app.crawler_links:
        crawler = crawler_list[link]
        if crawler in checked:
            logger.info('A crawler for "%s" already exists', link)
        else:
            checked[crawler] = True
            futures_to_check[executor.submit(get_search_result, app.user_input, link)] = str(crawler)

    bar = IncrementalBar('Searching', max=(len(futures_to_check.keys())))
    bar.start()
    if os.getenv('debug_mode') == 'yes':
        bar.next = lambda : None
    app.progress = 0
    combined_results = []
    for future in futures.as_completed(futures_to_check):
        combined_results += future.result()
        app.progress += 1
        bar.next()

    app.search_results = process_results(combined_results)
    bar.clearln()
    bar.finish()
    print('Found %d results' % len(app.search_results))
    executor.shutdown()