# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/bots/console/get_crawler.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 3003 bytes
import re
from PyInquirer import prompt
from ...core import display
from ...core.arguments import get_args
from ...sources import rejected_sources

def get_novel_url(self):
    """Returns a novel page url or a query"""
    args = get_args()
    if args.query:
        if len(args.query) > 1:
            return args.query
    url = args.novel_page
    if url:
        if re.match('^https?://.+\\..+$', url):
            return url
        raise Exception('Invalid URL of novel page')
    try:
        if args.suppress:
            raise Exception()
        answer = prompt([
         {'type':'input', 
          'name':'novel', 
          'message':'Enter novel page url or query novel:', 
          'validate':lambda val: 'Input should not be empty' if len(val) == 0 else True}])
        return answer['novel'].strip()
    except Exception:
        raise Exception('Novel page url or query was not given')


def get_crawlers_to_search(self):
    """Returns user choice to search the choosen sites for a novel"""
    links = self.app.crawler_links
    if not links:
        return
    args = get_args()
    if args.suppress or not args.sources:
        return links
    else:
        answer = prompt([
         {'type':'checkbox', 
          'name':'sites', 
          'message':'Where to search?', 
          'choices':[{'name': x} for x in sorted(links)]}])
        selected = answer['sites']
        if len(selected) > 0:
            return selected
        return links


def choose_a_novel(self):
    """Choose a single novel url from the search result"""
    args = get_args()
    choices = self.app.search_results
    selected_choice = self.app.search_results[0]
    if len(choices) > 1:
        if not args.suppress:
            answer = prompt([
             {'type':'list', 
              'name':'novel', 
              'message':'Which one is your novel?', 
              'choices':display.format_novel_choices(choices)}])
            index = int(answer['novel'].split('.')[0])
            selected_choice = self.app.search_results[(index - 1)]
    else:
        novels = selected_choice['novels']
        selected_novel = novels[0]
        if len(novels) > 1:
            if not args.suppress:
                answer = prompt([
                 {'type':'list', 
                  'name':'novel', 
                  'message':'Choose a source to download?', 
                  'choices':[
                   '0. Back'] + display.format_source_choices(novels)}])
                index = int(answer['novel'].split('.')[0])
                if index == 0:
                    return self.choose_a_novel()
                selected_novel = novels[(index - 1)]
    return selected_novel['url']