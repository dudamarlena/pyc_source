# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\test\test_crawler.py
# Compiled at: 2020-04-12 13:14:01
# Size of source mod 2**32: 2550 bytes
import os
from core.app import App
from ...binders import available_formats

def test_crawler(self, link, user_input):
    app = App()
    print('App instance: OK')
    app.initialize()
    print('App initialize: DONE')
    app.user_input = user_input
    app.init_search()
    print('Init search: DONE')
    if not app.crawler:
        if link not in app.crawler_links:
            print('Search is not supported for', link)
            return None
        print(len(app.crawler_links), 'available crawlers to search')
        app.crawler_links = [link]
        print('Selected crawler:', link)
        app.search_novel()
        print('Search: %d results found' % len(app.search_results))
        source = app.search_results[0]
        print('Top result: %s with %d sources' % (
         source['title'], len(source['novels'])))
        novel_url = source['novels'][0]['url']
        print('Top novel:', novel_url)
        app.init_crawler(novel_url)
        print('Init crawler: DONE')
        app.get_novel_info()
        print('Novel info: DONE')
        if not app.crawler.novel_title:
            raise Exception('No novel title')
        return
    if not app.crawler:
        raise Exception('No crawler initialized')
    if app.can_do('login'):
        print('Login: enabled')
    app.get_novel_info()
    print('Title:', app.crawler.novel_title)
    print('Cover:', app.crawler.novel_cover)
    print('Author:', app.crawler.novel_author)
    if not app.crawler.novel_title:
        raise Exception('No novel title')
    print('Novel info: DONE')
    os.makedirs((app.output_path), exist_ok=True)
    print('Output path:', app.output_path)
    if len(app.crawler.volumes) == 0:
        raise Exception('Empty volume list')
    if len(app.crawler.chapters) == 0:
        raise Exception('Empty chapter list')
    app.chapters = app.crawler.chapters[:2]
    app.output_formats = {False:x for x in available_formats}
    app.output_formats['pdf'] = True
    app.pack_by_volume = False
    app.start_download()
    print('Download: DONE')
    if len(app.chapters[0]['body']) < 50:
        raise Exception('Empty body')
    app.bind_books()
    print('Bindings: DONE')
    app.destroy()
    print('Destroy: DONE')
    print('------', 'Test Passed', '------')