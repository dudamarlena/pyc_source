# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\console.py
# Compiled at: 2019-11-14 16:20:14
# Size of source mod 2**32: 20260 bytes
import logging, os, re, shutil
from urllib.parse import urlparse
from PyInquirer import prompt
from ..binders import available_formats
from ..core import display
from core.app import App
from core.arguments import get_args
from ..spiders import rejected_sources
logger = logging.getLogger('CONSOLE_INTERFACE')

class ConsoleBot:

    def start(self):
        args = get_args()
        if args.list_sources:
            display.url_supported_list()
            return
        self.app = App()
        self.app.initialize()
        self.app.user_input = self.get_novel_url()
        try:
            self.app.init_search()
        except Exception:
            if self.app.user_input.startswith('http'):
                url = urlparse(self.app.user_input)
                url = '%s://%s/' % (url.scheme, url.hostname)
                if url in rejected_sources:
                    display.url_rejected(rejected_sources[url])
                    return
            display.url_not_recognized()
            return
        else:
            if not self.app.crawler:
                self.app.crawler_links = self.get_crawlers_to_search()
                self.app.search_novel()
                novel_url = self.choose_a_novel()
                logger.info('Selected novel: %s' % novel_url)
                self.app.init_crawler(novel_url)
            if self.app.can_do('login'):
                self.app.login_data = self.get_login_info()
            self.app.get_novel_info()
            self.app.output_path = self.get_output_path()
            self.app.chapters = self.process_chapter_range()
            self.app.output_formats = self.get_output_formats()
            self.app.pack_by_volume = self.should_pack_by_volume()
            self.app.start_download()
            self.app.bind_books()
            self.app.destroy()
            display.app_complete()
            if self.open_folder():
                import pathlib, webbrowser
                url = pathlib.Path(self.app.output_path).as_uri()
                webbrowser.open_new(url)

    def process_chapter_range(self):
        chapters = []
        res = self.get_range_selection()
        args = get_args()
        if res == 'all':
            chapters = self.app.crawler.chapters[:]
        else:
            if res == 'first':
                n = args.first or 10
                chapters = self.app.crawler.chapters[:n]
            else:
                if res == 'last':
                    n = args.last or 10
                    chapters = self.app.crawler.chapters[-n:]
                else:
                    if res == 'page':
                        start, stop = self.get_range_using_urls()
                        chapters = self.app.crawler.chapters[start:stop + 1]
                    else:
                        if res == 'range':
                            start, stop = self.get_range_using_index()
                            chapters = self.app.crawler.chapters[start:stop + 1]
                        else:
                            if res == 'volumes':
                                selected = self.get_range_from_volumes()
                                chapters = [chap for chap in self.app.crawler.chapters if selected.count(chap['volume']) > 0]
                            else:
                                if res == 'chapters':
                                    selected = self.get_range_from_chapters()
                                    chapters = [chap for chap in self.app.crawler.chapters if selected.count(chap['id']) > 0]
                                else:
                                    if len(chapters) == 0:
                                        raise Exception('No chapters to download')
                                    logger.debug('Selected chapters:')
                                    logger.debug(chapters)
                                    if not args.suppress:
                                        answer = prompt([
                                         {'type':'list', 
                                          'name':'continue', 
                                          'message':'%d chapters selected' % len(chapters), 
                                          'choices':[
                                           'Continue',
                                           'Change selection']}])
                                        if answer['continue'] == 'Change selection':
                                            return self.process_chapter_range()
                                logger.info('%d chapters to be downloaded', len(chapters))
                                return chapters

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
              'validate':lambda val:               if len(val) == 0:
'Input should not be empty' # Avoid dead code: True}])
            return answer['novel'].strip()
        except Exception:
            raise Exception('Novel page url or query was not given')

    def get_crawlers_to_search(self):
        """Returns user choice to search the choosen sites for a novel"""
        links = self.app.crawler_links
        if not links:
            return
        else:
            args = get_args()
            return args.suppress or args.sources or links
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
                answer = args.suppress or prompt([
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

    def get_login_info(self):
        """Returns the (email, password) pair for login"""
        args = get_args()
        if args.login:
            return args.login
        if args.suppress:
            return False
        answer = prompt([
         {'type':'confirm', 
          'name':'login', 
          'message':'Do you want to log in?', 
          'default':False}])
        if answer['login']:
            answer = prompt([
             {'type':'input', 
              'name':'email', 
              'message':'Email:', 
              'validate':lambda val:               if len(val):
True # Avoid dead code: 'Email address should be not be empty'},
             {'type':'password', 
              'name':'password', 
              'message':'Password:', 
              'validate':lambda val:               if len(val):
True # Avoid dead code: 'Password should be not be empty'}])
            return (
             answer['email'], answer['password'])

    def get_output_path(self):
        """Returns a valid output path where the files are stored"""
        args = get_args()
        output_path = args.output_path
        if args.suppress:
            if not output_path:
                output_path = self.app.output_path
            if not output_path:
                output_path = os.path.join('Lightnovels', 'Unknown Novel')
        if not output_path:
            answer = prompt([
             {'type':'input', 
              'name':'output', 
              'message':'Enter output direcotry:', 
              'default':os.path.abspath(self.app.output_path)}])
            output_path = answer['output']
        output_path = os.path.abspath(output_path)
        if os.path.exists(output_path):
            if self.force_replace_old():
                shutil.rmtree(output_path, ignore_errors=True)
        os.makedirs(output_path, exist_ok=True)
        return output_path

    def force_replace_old(self):
        args = get_args()
        if args.force:
            return True
        if args.ignore:
            return False
        if args.suppress:
            return False
        answer = prompt([
         {'type':'list', 
          'name':'replace', 
          'message':'What to do with existing folder?', 
          'choices':[
           'Remove old folder and start fresh',
           'Download remaining chapters only']}])
        return answer['replace'].startswith('remove')

    def get_output_formats(self):
        """Returns a dictionary of output formats."""
        args = get_args()
        formats = args.output_formats
        if not formats:
            if not args.suppress:
                answer = prompt([
                 {'type':'checkbox', 
                  'name':'formats', 
                  'message':'Which output formats to create?', 
                  'choices':[{'name': x} for x in available_formats]}])
                formats = answer['formats']
        if not formats or len(formats) == 0:
            formats = available_formats
        return {x:formats.count(x) > 0 for x in available_formats}

    def should_pack_by_volume(self):
        """Returns whether to generate single or multiple files by volumes"""
        args = get_args()
        if args.single:
            return False
        if args.multi:
            return True
        if args.suppress:
            return False
        answer = prompt([
         {'type':'list', 
          'name':'split', 
          'message':'How many files to generate?', 
          'choices':[
           'Pack everything into a single file',
           'Split by volume into multiple files']}])
        return answer['split'].startswith('Split')

    def get_range_selection(self):
        """
        Returns a choice of how to select the range of chapters to downloads
        """
        volume_count = len(self.app.crawler.volumes)
        chapter_count = len(self.app.crawler.chapters)
        selections = ['all', 'last', 'first',
         'page', 'range', 'volumes', 'chapters']
        args = get_args()
        for key in selections:
            if args.__getattribute__(key):
                return key

        if args.suppress:
            return selections[0]
        big_list_warn = '(warn: very big list)' if chapter_count > 50 else ''
        choices = [
         'Everything! (%d chapters)' % chapter_count,
         'Last 10 chapters',
         'First 10 chapters',
         'Custom range using URL',
         'Custom range using index',
         'Select specific volumes (%d volumes)' % volume_count,
         'Select specific chapters ' + big_list_warn]
        if chapter_count <= 20:
            choices.pop(1)
            choices.pop(1)
        answer = prompt([
         {'type':'list', 
          'name':'choice', 
          'message':'Which chapters to download?', 
          'choices':choices}])
        return selections[choices.index(answer['choice'])]

    def get_range_using_urls(self):
        """Returns a range of chapters using start and end urls as input"""
        args = get_args()
        start_url, stop_url = args.page or (None, None)
        if args.suppress:
            return start_url and stop_url or (
             0, len(self.app.crawler.chapters) - 1)
        if not (start_url and stop_url):

            def validator(val):
                try:
                    if self.app.crawler.get_chapter_index_of(val) > 0:
                        return True
                except Exception:
                    pass

                return 'No such chapter found given the url'

            answer = prompt([
             {'type':'input', 
              'name':'start_url', 
              'message':'Enter start url:', 
              'validate':validator},
             {'type':'input', 
              'name':'stop_url', 
              'message':'Enter final url:', 
              'validate':validator}])
            start_url = answer['start_url']
            stop_url = answer['stop_url']
        start = self.app.crawler.get_chapter_index_of(start_url) - 1
        stop = self.app.crawler.get_chapter_index_of(stop_url) - 1
        if start < stop:
            return (start, stop)
        return (stop, start)

    def get_range_using_index(self):
        """Returns a range selected using chapter indices"""
        chapter_count = len(self.app.crawler.chapters)
        args = get_args()
        start, stop = args.range or (None, None)
        if args.suppress:
            return start and stop or (
             0, chapter_count - 1)
        elif not (start and stop):

            def validator(val):
                try:
                    if 1 <= int(val) <= chapter_count:
                        return True
                except Exception:
                    pass

                return 'Enter an integer between 1 and %d' % chapter_count

            answer = prompt([
             {'type':'input', 
              'name':'start', 
              'message':'Enter start index (1 to %d):' % chapter_count, 
              'validate':validator, 
              'filter':lambda val: int(val)},
             {'type':'input', 
              'name':'stop', 
              'message':'Enter final index (1 to %d):' % chapter_count, 
              'validate':validator, 
              'filter':lambda val: int(val)}])
            start = answer['start'] - 1
            stop = answer['stop'] - 1
        else:
            start = start - 1
            stop = stop - 1
        if start < stop:
            return (start, stop)
        return (stop, start)

    def get_range_from_volumes(self, times=0):
        """Returns a range created using volume list"""
        selected = None
        args = get_args()
        if times == 0:
            if args.volumes:
                selected = [int(x) for x in args.volumes]
        if not selected:
            if args.suppress:
                selected = [x['id'] for x in self.app.crawler.volumes]
        if not selected:
            answer = prompt([
             {'type':'checkbox', 
              'name':'volumes', 
              'message':'Choose volumes to download:', 
              'choices':[{'name': '%d - %s [%d chapters]' % (vol['id'], vol['title'], vol['chapter_count'])} for vol in self.app.crawler.volumes], 
              'validate':lambda ans:               if len(ans) > 0:
True # Avoid dead code: 'You must choose at least one volume.'}])
            selected = [int(val.split(' ')[0]) for val in answer['volumes']]
        if times < 3:
            if len(selected) == 0:
                return self.get_range_from_volumes(times + 1)
        return selected

    def get_range_from_chapters(self, times=0):
        """Returns a range created using individual chapters"""
        selected = None
        args = get_args()
        if times == 0:
            if not selected:
                selected = get_args().chapters
        if not selected:
            if args.suppress:
                selected = self.app.crawler.chapters
        elif not selected:
            answer = prompt([
             {'type':'checkbox', 
              'name':'chapters', 
              'message':'Choose chapters to download:', 
              'choices':[{'name': '%d - %s' % (chap['id'], chap['title'])} for chap in self.app.crawler.chapters], 
              'validate':lambda ans:               if len(ans) > 0:
True # Avoid dead code: 'You must choose at least one chapter.'}])
            selected = [int(val.split(' ')[0]) for val in answer['chapters']]
        else:
            selected = [self.app.crawler.get_chapter_index_of(x) for x in selected if x]
        if times < 3:
            if len(selected) == 0:
                return self.get_range_from_chapters(times + 1)
        selected = [x for x in selected if 1 <= x <= len(self.app.crawler.chapters)]
        return selected

    def open_folder(self):
        args = get_args()
        if args.suppress:
            return False
        answer = prompt([
         {'type':'confirm', 
          'name':'exit', 
          'message':'Open the output folder?', 
          'default':True}])
        return answer['exit']