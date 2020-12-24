# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\zenithnovels.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3201 bytes
import json, logging, re, requests
from utils.crawler import Crawler
logger = logging.getLogger('ZENITH_NOVELS')
novel_url = 'http://zenithnovels.com/%s/'

class ZenithNovelsCrawler(Crawler):
    base_url = 'http://zenithnovels.com/'

    def read_novel_info--- This code section failed: ---

 L.  20         0  LOAD_GLOBAL              re
                2  LOAD_METHOD              search

 L.  21         4  LOAD_STR                 '(?<=zenithnovels.com/)[^/]+'

 L.  21         6  LOAD_FAST                'self'
                8  LOAD_ATTR                novel_url

 L.  20        10  CALL_METHOD_2         2  ''
               12  LOAD_METHOD              group

 L.  21        14  LOAD_CONST               0

 L.  20        16  CALL_METHOD_1         1  ''
               18  LOAD_FAST                'self'
               20  STORE_ATTR               novel_id

 L.  22        22  LOAD_GLOBAL              logger
               24  LOAD_METHOD              info
               26  LOAD_STR                 'Novel id: %s'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                novel_id
               32  CALL_METHOD_2         2  ''
               34  POP_TOP          

 L.  24        36  LOAD_GLOBAL              novel_url
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                novel_id
               42  BINARY_MODULO    
               44  STORE_FAST               'url'

 L.  25        46  LOAD_GLOBAL              logger
               48  LOAD_METHOD              debug
               50  LOAD_STR                 'Visiting %s'
               52  LOAD_FAST                'url'
               54  CALL_METHOD_2         2  ''
               56  POP_TOP          

 L.  26        58  LOAD_FAST                'self'
               60  LOAD_METHOD              get_soup
               62  LOAD_FAST                'url'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'soup'

 L.  28        68  LOAD_FAST                'soup'
               70  LOAD_METHOD              select_one
               72  LOAD_STR                 'article#the-post h1.name'
               74  CALL_METHOD_1         1  ''
               76  LOAD_ATTR                text
               78  LOAD_FAST                'self'
               80  STORE_ATTR               novel_title

 L.  29        82  LOAD_GLOBAL              logger
               84  LOAD_METHOD              info
               86  LOAD_STR                 'Novel title: %s'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                novel_title
               92  CALL_METHOD_2         2  ''
               94  POP_TOP          

 L.  31        96  LOAD_FAST                'self'
               98  LOAD_METHOD              absolute_url
              100  LOAD_FAST                'soup'
              102  LOAD_METHOD              select_one

 L.  32       104  LOAD_STR                 'article#the-post .entry img'

 L.  31       106  CALL_METHOD_1         1  ''

 L.  32       108  LOAD_STR                 'src'

 L.  31       110  BINARY_SUBSCR    
              112  CALL_METHOD_1         1  ''
              114  LOAD_FAST                'self'
              116  STORE_ATTR               novel_cover

 L.  33       118  LOAD_GLOBAL              logger
              120  LOAD_METHOD              info
              122  LOAD_STR                 'Novel cover: %s'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                novel_cover
              128  CALL_METHOD_2         2  ''
              130  POP_TOP          

 L.  36       132  LOAD_FAST                'self'
              134  LOAD_METHOD              parse_chapter_list
              136  LOAD_FAST                'soup'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L.  38       142  LOAD_FAST                'soup'
              144  LOAD_METHOD              select_one
              146  LOAD_STR                 'ul.lcp_paginator a.lcp_nextlink'
              148  CALL_METHOD_1         1  ''
              150  STORE_FAST               'next_link'

 L.  39       152  LOAD_FAST                'next_link'
              154  POP_JUMP_IF_FALSE   176  'to 176'

 L.  40       156  LOAD_FAST                'self'
              158  LOAD_METHOD              get_soup
              160  LOAD_FAST                'next_link'
              162  LOAD_STR                 'href'
              164  BINARY_SUBSCR    
              166  CALL_METHOD_1         1  ''
              168  STORE_FAST               'soup'
              170  JUMP_BACK           132  'to 132'

 L.  42       172  BREAK_LOOP          176  'to 176'
              174  JUMP_BACK           132  'to 132'
            176_0  COME_FROM           154  '154'

 L.  46       176  LOAD_FAST                'self'
              178  LOAD_ATTR                chapters
              180  LOAD_ATTR                sort
              182  LOAD_LAMBDA              '<code_object <lambda>>'
              184  LOAD_STR                 'ZenithNovelsCrawler.read_novel_info.<locals>.<lambda>'
              186  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              188  LOAD_CONST               ('key',)
              190  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              192  POP_TOP          

 L.  47       194  LOAD_LISTCOMP            '<code_object <listcomp>>'
              196  LOAD_STR                 'ZenithNovelsCrawler.read_novel_info.<locals>.<listcomp>'
              198  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              200  LOAD_GLOBAL              set
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                volumes
              206  CALL_FUNCTION_1       1  ''
              208  GET_ITER         
              210  CALL_FUNCTION_1       1  ''
              212  LOAD_FAST                'self'
              214  STORE_ATTR               volumes

Parse error at or near `LOAD_FAST' instruction at offset 212

    def parse_chapter_list(self, soup):
        for a in soup.select('ul.lcp_catlist li a'):
            ch_title = a['title']
            ch_id = [int(''.join(x).strip()) for x in re.findall('((?<=ch) \\d+)|((?<=chapter) \\d+)', ch_title, re.IGNORECASE)]
            ch_id = ch_id[0] if len(ch_id) else len(self.chapters) + 1
            vol_id = [int(''.join(x).strip()) for x in re.findall('((?<=book) \\d+)|((?<=volume) \\d+)', ch_title, re.IGNORECASE)]
            vol_id = vol_id[0] if len(vol_id) else 1 + (ch_id - 1) // 100
            self.volumes.append(vol_id)
            self.chapters.append({'id':ch_id, 
             'volume':vol_id, 
             'title':ch_title, 
             'url':self.absolute_url(a['href'])})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info'Downloading %s'chapter['url']
        soup = self.get_soup(chapter['url'])
        entry = soup.select_one('article#the-post .entry')
        try:
            self.clean_contents(entry)
            for note in entry.select('.footnote'):
                note.decompose()

        except Exception:
            pass
        else:
            body = ''
            for tag in entry.children:
                if tag.name == 'p' and len(tag.text.strip()):
                    p = ' '.join(self.extract_contents(tag))
                    if len(p.strip()):
                        body += '<p>%s</p>' % p
                return body