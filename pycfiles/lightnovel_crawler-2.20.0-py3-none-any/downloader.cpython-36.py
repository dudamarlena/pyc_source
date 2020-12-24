# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/core/downloader.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 5253 bytes
"""
To download chapter bodies
"""
import json, logging, os
from concurrent import futures
from io import BytesIO
from urllib.parse import urlparse
from PIL import Image
from progress.bar import IncrementalBar
from ..core.arguments import get_args
from ..utils.racovimge import random_cover
logger = logging.getLogger('DOWNLOADER')
try:
    from cairosvg import svg2png
except Exception:
    svg2png = None
    logger.info('CairoSVG was not found.Install it to generate random cover image:\n    pip install cairosvg')

def download_cover(app):
    if not app.crawler.novel_cover:
        return
    filename = None
    try:
        filename = os.path.join(app.output_path, 'cover.png')
        if os.path.exists(filename):
            return filename
    except Exception as ex:
        logger.warn('Failed to locate cover image: %s -> %s (%s)', app.crawler.novel_cover, app.output_path, str(ex))
        return

    try:
        logger.info('Downloading cover image...')
        response = app.crawler.get_response(app.crawler.novel_cover)
        assert response.status_code == 200
        img = Image.open(BytesIO(response.content))
        img.save(filename)
        logger.debug('Saved cover: %s', filename)
        return filename
    except Exception as ex:
        logger.warn('Failed to download cover image: %s -> %s (%s)', app.crawler.novel_cover, filename, str(ex))
        return


def generate_cover(app):
    logger.info('Generating cover image...')
    if svg2png is None:
        return
    try:
        svg_file = os.path.join(app.output_path, 'cover.svg')
        svg = random_cover(title=(app.crawler.novel_title),
          author=(app.crawler.novel_author))
        with open(svg_file, 'w', encoding='utf-8') as (f):
            f.write(svg)
            logger.debug('Saved a random cover.svg')
        png_file = os.path.join(app.output_path, 'cover.png')
        svg2png(bytestring=(svg.encode('utf-8')), write_to=png_file)
        logger.debug('Converted cover.svg to cover.png')
        return png_file
    except Exception:
        logger.exception('Failed to generate cover image: %s', app.output_path)
        return


def download_chapter_body(app, chapter):
    result = None
    dir_name = os.path.join(app.output_path, 'json')
    if app.pack_by_volume:
        vol_name = 'Volume ' + str(chapter['volume']).rjust(2, '0')
        dir_name = os.path.join(dir_name, vol_name)
    os.makedirs(dir_name, exist_ok=True)
    chapter_name = str(chapter['id']).rjust(5, '0')
    file_name = os.path.join(dir_name, chapter_name + '.json')
    chapter['body'] = ''
    if os.path.exists(file_name):
        logger.debug('Restoring from %s', file_name)
        with open(file_name, 'r', encoding='utf-8') as (file):
            old_chapter = json.load(file)
            chapter['body'] = old_chapter['body']
    if len(chapter['body']) == 0:
        body = ''
        try:
            logger.debug('Downloading to %s', file_name)
            body = app.crawler.download_chapter_body(chapter)
        except Exception:
            logger.exception('Failed to download chapter body')

        if len(body) == 0:
            result = 'Body is empty: ' + chapter['url']
        else:
            if not ('body_lock' in chapter and chapter['body_lock']):
                body = app.crawler.cleanup_text(body)
        title = chapter['title'].replace('>', '&gt;').replace('<', '&lt;')
        chapter['body'] = '<h1>%s</h1>\n%s' % (title, body)
        if get_args().add_source_url:
            chapter['body'] += '<br><p>Source: <a href="%s">%s</a></p>' % (
             chapter['url'], chapter['url'])
        with open(file_name, 'w', encoding='utf-8') as (file):
            file.write(json.dumps(chapter))
    return result


def download_chapters(app):
    app.book_cover = download_cover(app)
    if not app.book_cover:
        app.book_cover = generate_cover(app)
    if not app.book_cover:
        logger.warn('No cover image')
    bar = IncrementalBar('Downloading chapters', max=(len(app.chapters)))
    bar.start()
    if os.getenv('debug_mode') == 'yes':
        bar.next = lambda : None
    futures_to_check = {app.crawler.executor.submit(download_chapter_body, app, chapter):str(chapter['id']) for chapter in app.chapters}
    app.progress = 0
    for future in futures.as_completed(futures_to_check):
        result = future.result()
        if result:
            bar.clearln()
            logger.error(result)
        app.progress += 1
        bar.next()

    bar.finish()
    print('Downloaded %d chapters' % len(app.chapters))