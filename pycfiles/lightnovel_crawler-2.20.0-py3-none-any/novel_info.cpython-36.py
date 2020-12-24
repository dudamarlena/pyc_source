# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/core/novel_info.py
# Compiled at: 2020-03-23 11:49:43
# Size of source mod 2**32: 2190 bytes
"""
To get the novel info
"""
import re, os, json
from ..utils.crawler import Crawler

def format_novel(crawler: Crawler):
    crawler.novel_title = crawler.novel_title.strip()
    crawler.novel_author = crawler.novel_author.strip()
    format_volumes(crawler)
    format_chapters(crawler)


def format_volumes(crawler: Crawler):
    for vol in crawler.volumes:
        vol['chapter_count'] = 0
        vol['final_chapter'] = 0
        vol['start_chapter'] = 100000000.0
        title = 'Volume %d' % vol['id']
        if not ('title' in vol and vol['title']):
            vol['title'] = title


def format_chapters(crawler: Crawler):
    for item in crawler.chapters:
        title = '#%d' % item['id']
        if not ('title' in item and item['title']):
            item['title'] = title
        volume = [x for x in crawler.volumes if x['id'] == item['volume']]
        if len(volume) == 0:
            raise Exception('Unknown volume %s for chapter %s' % (item['volume'], item['id']))
        else:
            volume = volume[0]
        item['volume_title'] = volume['title']
        volume['chapter_count'] += 1
        volume['final_chapter'] = item['id'] if volume['final_chapter'] < item['id'] else volume['final_chapter']
        volume['start_chapter'] = item['id'] if volume['start_chapter'] > item['id'] else volume['start_chapter']


def save_metadata(crawler, output_path):
    data = {'url':crawler.novel_url, 
     'title':crawler.novel_title, 
     'author':crawler.novel_author, 
     'cover':crawler.novel_cover, 
     'volumes':crawler.volumes, 
     'chapters':crawler.chapters, 
     'rtl':crawler.is_rtl}
    file_name = os.path.join(output_path, 'json', 'meta.json')
    os.makedirs((os.path.dirname(file_name)), exist_ok=True)
    with open(file_name, 'w', encoding='utf-8') as (file):
        json.dump(data, file, indent=2)