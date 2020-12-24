# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\discord\message_handler.py
# Compiled at: 2020-04-07 07:28:02
# Size of source mod 2**32: 20035 bytes
import asyncio, logging, os, random, re, shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import quote
import discord
from core.app import App
from ...sources import crawler_list
from utils.uploader import upload
from .config import max_workers, public_ip, public_path
logger = logging.getLogger(__name__)
available_formats = [
 'epub',
 'text',
 'web',
 'mobi',
 'pdf']
disable_search = os.getenv('DISCORD_DISABLE_SEARCH') == 'true'

class MessageHandler:

    def __init__(self, client):
        self.app = App()
        self.client = client
        self.state = None
        self.executor = ThreadPoolExecutor(max_workers)
        self.last_activity = datetime.now()

    def process(self, message):
        self.last_activity = datetime.now()
        self.executor.submit(self.handle_message, message)

    def destroy(self):
        try:
            try:
                self.client.handlers.pop(str(self.user.id))
                self.send_sync('Closing current session...')
                self.executor.shutdown(wait=False)
                self.app.destroy()
            except Exception:
                logger.exception('While destroying MessageHandler')

        finally:
            self.send_sync('Session closed. Send *start* to start over')

    def handle_message(self, message):
        self.message = message
        self.user = message.author
        if not self.state:
            self.state = self.get_novel_url
        try:
            self.state()
        except Exception as ex:
            try:
                logger.exception('Failed to process state')
                self.send_sync('Something went wrong!\n`%s`' % str(ex))
                self.executor.submit(self.destroy)
            finally:
                ex = None
                del ex

    def wait_for(self, async_coroutine):
        asyncio.run_coroutine_threadsafe(async_coroutine, self.client.loop).result()

    async def send--- This code section failed: ---

 L.  85         0  LOAD_GLOBAL              datetime
                2  LOAD_METHOD              now
                4  CALL_METHOD_0         0  ''
                6  LOAD_FAST                'self'
                8  STORE_ATTR               last_activity

 L.  86        10  LOAD_FAST                'self'
               12  LOAD_ATTR                user
               14  LOAD_METHOD              typing
               16  CALL_METHOD_0         0  ''
               18  BEFORE_ASYNC_WITH
               20  GET_AWAITABLE    
               22  LOAD_CONST               None
               24  YIELD_FROM       
               26  SETUP_ASYNC_WITH     68  'to 68'
               28  POP_TOP          

 L.  87        30  LOAD_FAST                'contents'
               32  GET_ITER         
               34  FOR_ITER             64  'to 64'
               36  STORE_FAST               'text'

 L.  88        38  LOAD_FAST                'text'
               40  POP_JUMP_IF_TRUE     44  'to 44'

 L.  89        42  JUMP_BACK            34  'to 34'
             44_0  COME_FROM            40  '40'

 L.  91        44  LOAD_FAST                'self'
               46  LOAD_ATTR                user
               48  LOAD_METHOD              send
               50  LOAD_FAST                'text'
               52  CALL_METHOD_1         1  ''
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  POP_TOP          
               62  JUMP_BACK            34  'to 34'
               64  POP_BLOCK        
               66  BEGIN_FINALLY    
             68_0  COME_FROM_ASYNC_WITH    26  '26'
               68  WITH_CLEANUP_START
               70  GET_AWAITABLE    
               72  LOAD_CONST               None
               74  YIELD_FROM       
               76  WITH_CLEANUP_FINISH
               78  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 68_0

    def send_sync(self, *contents):
        self.wait_for((self.send)(*contents))

    def busy_state(self):
        text = self.message.content.strip()
        if text == '!cancel':
            self.executor.submit(self.destroy)
            return None
        self.send_sync(random.choice([
         'Send !cancel to stop this session.',
         'Please wait...',
         'Processing, give me more time...',
         'I am just a bot. Please be patient...',
         'Waiting for more RAM...',
         'A little bit longer...',
         "I'll be with you in a bit...",
         'Patience! This is difficult, you know...']))

    def get_novel_url(self):
        self.state = self.busy_state
        if disable_search:
            self.send_sync('Send me an URL of novel info page with chapter list!')
        else:
            self.send_sync('I recognize these two categories:\n- Profile page url of a lightnovel.\n- A query to search your lightnovel.', 'What are you looking for?')
        self.state = self.handle_novel_url

    def handle_novel_url(self):
        self.state = self.busy_state
        text = self.message.content.strip()
        if text == '!cancel':
            self.executor.submit(self.destroy)
            return None
        try:
            self.app.user_input = self.message.content.strip()
            self.app.init_search()
        except Exception:
            self.send_sync('\n'.join([
             'Sorry! I do not recognize this sources yet.',
             'See list of supported sources here:',
             'https://github.com/dipu-bd/lightnovel-crawler#c3-supported-sources']))
            self.get_novel_url()
        else:
            if self.app.crawler:
                self.send_sync('Got your page link')
                self.get_novel_info()
            else:
                if len(self.app.user_input) < 4:
                    self.send_sync('Your query is too short')
                    self.state = self.handle_novel_url
                    self.get_novel_url()
                else:
                    if disable_search:
                        self.send_sync('Sorry! I can not do searching.\nPlease use Google to find your novel first')
                        self.get_novel_url()
                    else:
                        self.send_sync('Searching %d sources for "%s"\n' % (
                         len(self.app.crawler_links), self.app.user_input))
                        self.display_novel_selection()

    def display_novel_selection(self):
        self.app.search_novel()
        if len(self.app.search_results) == 0:
            self.send_sync('No novels found for "%s"' % self.app.user_input)
            self.state = self.handle_novel_url
        else:
            if len(self.app.search_results) == 1:
                self.selected_novel = self.app.search_results[0]
                self.display_sources_selection()
            else:
                self.send_sync('\n'.join([
                 'Found %d novels:\n' % len(self.app.search_results)] + ['%d. **%s** `%d sources`' % (
                 i + 1,
                 item['title'],
                 len(item['novels'])) for i, item in enumerate(self.app.search_results)] + [
                 'Enter name or index of your novel.',
                 'Send `!cancel` to stop this session.']))
                self.state = self.handle_novel_selection

    def handle_novel_selection(self):
        self.state = self.busy_state
        text = self.message.content.strip()
        if text.startswith('!cancel'):
            self.get_novel_url()
            return None
        match_count = 0
        selected = None
        for i, res in enumerate(self.app.search_results):
            if str(i + 1) == text:
                selected = res
                match_count += 1
        else:
            if not text.isdigit():
                if len(text) < 3:
                    pass
                elif res['title'].lower().find(text) != -1:
                    selected = res
                    match_count += 1
            if match_count != 1:
                self.send_sync('Sorry! You should select *one* novel from the list (%d selected).' % match_count)
                self.display_novel_selection()
                return None
            self.selected_novel = selected
            self.display_sources_selection()

    def display_sources_selection(self):
        self.send_sync('\n'.join([
         '**%s** is found in %d sources:\n' % (
          self.selected_novel['title'], len(self.selected_novel['novels']))] + ['%d. <%s> %s' % (
         i + 1,
         item['url'],
         item['info'] if 'info' in item else '') for i, item in enumerate(self.selected_novel['novels'])] + [
         'Enter index or name of your source.',
         'Send `!cancel` to stop this session.']))
        self.state = self.handle_sources_to_search

    def handle_sources_to_search(self):
        self.state = self.busy_state
        if len(self.selected_novel['novels']) == 1:
            novel = self.selected_novel['novels'][0]
            return self.handle_search_result(novel)
        text = self.message.content.strip()
        if text.startswith('!cancel'):
            return self.get_novel_url()
        match_count = 0
        selected = None
        for i, res in enumerate(self.selected_novel['novels']):
            if str(i + 1) == text:
                selected = res
                match_count += 1
        else:
            if not text.isdigit():
                if len(text) < 3:
                    pass
                elif res['url'].lower().find(text) != -1:
                    selected = res
                    match_count += 1
            if match_count != 1:
                self.send_sync('Sorry! You should select *one* source from the list (%d selected).' % match_count)
                return self.display_sources_selection()
            self.handle_search_result(selected)

    def handle_search_result(self, novel):
        self.send_sync('Selected: %s' % novel['url'])
        self.app.init_crawler(novel['url'])
        self.get_novel_info()

    def get_novel_info(self):
        self.send_sync('Getting information about your novel...')
        self.executor.submit(self.download_novel_info)

    def download_novel_info(self):
        self.state = self.busy_state
        try:
            self.app.get_novel_info()
        except Exception as ex:
            try:
                logger.exception('Failed to get novel info')
                self.send_sync('Failed to get novel info.\n`%s`' % str(ex))
                self.executor.submit(self.destroy)
            finally:
                ex = None
                del ex

        else:
            root = os.path.abspath('.discord_bot_output')
            if public_path:
                if os.path.exists(public_path):
                    root = os.path.abspath(public_path)
            good_name = os.path.basename(self.app.output_path)
            output_path = os.path.join(root, str(self.user.id), good_name)
            if os.path.exists(output_path):
                shutil.rmtree(output_path, ignore_errors=True)
            os.makedirs(output_path, exist_ok=True)
            self.app.output_path = output_path
            self.display_range_selection()

    def display_range_selection(self):
        self.send_sync('\n'.join([
         'Now you choose what to download:',
         '- Send `!cancel` to stop this session.',
         '- Send `all` to download all chapters',
         '- Send `last 20` to download last 20 chapters. Choose any number you want.',
         '- Send `first 10` for first 10 chapters. Choose any number you want.',
         '- Send `volume 2 5` to download download volume 2 and 5. Pass as many numbers you need.',
         '- Send `chapter 110 120` to download chapter 110 to 120. Only two numbers are accepted.']))
        self.send_sync('**It has `%d` volumes and `%d` chapters.**' % (
         len(self.app.crawler.volumes),
         len(self.app.crawler.chapters)))
        self.state = self.handle_range_selection

    def handle_range_selection(self):
        self.state = self.busy_state
        text = self.message.content.strip()
        if text == '!cancel':
            self.executor.submit(self.destroy)
            return
            if text == 'all':
                self.app.chapters = self.app.crawler.chapters[:]
        elif re.match('^first(\\s\\d+)?$', text):
            text = text[len('first'):].strip()
            n = int(text) if text.isdigit() else 50
            n = 50 if n < 0 else n
            self.app.chapters = self.app.crawler.chapters[:n]
        else:
            if re.match('^last(\\s\\d+)?$', text):
                text = text[len('last'):].strip()
                n = int(text) if text.isdigit() else 50
                n = 50 if n < 0 else n
                self.app.chapters = self.app.crawler.chapters[-n:]
            else:
                if re.match('^volume(\\s\\d+)+$', text):
                    text = text[len('volume'):].strip()
                    selected = re.findall('\\d+', text)
                    self.send_sync('Selected volumes: ' + ', '.join(selected))
                    selected = [int(x) for x in selected]
                    self.app.chapters = [chap for chap in self.app.crawler.chapters if selected.count(chap['volume']) > 0]
                else:
                    if re.match('^chapter(\\s\\d+)+$', text):
                        text = text[len('chapter'):].strip()
                        pair = text.split(' ')
                        if len(pair) == 2:

                            def resolve_chapter(name):
                                cid = 0
                                if name.isdigit():
                                    cid = int(name)
                                else:
                                    cid = self.app.crawler.get_chapter_index_of(name)
                                return cid - 1

                            first = resolve_chapter(pair[0])
                            second = resolve_chapter(pair[1])
                            if first > second:
                                second, first = first, second
                            if first >= 0 or second < len(self.app.crawler.chapters):
                                self.app.chapters = self.app.crawler.chapters[first:second]
                        if len(self.app.chapters) == 0:
                            self.send_sync('Chapter range is not valid. Please try again')
                            self.state = self.handle_range_selection
                            return
                    else:
                        self.send_sync('Sorry! I did not recognize your input. Please try again')
                        self.state = self.handle_range_selection
                        return
        if len(self.app.chapters) == 0:
            self.send_sync('You have not selected any chapters. Please select at least one')
            self.state = self.handle_range_selection
            return
        self.send_sync('Got your range selection')
        self.display_output_selection()

    def display_output_selection(self):
        self.state = self.busy_state
        self.send_sync('\n'.join([
         'Now you can choose book formats to download:',
         '- Send `!cancel` to stop.',
         'To select specific output formats:',
         '- Send `pdf` to download only pdf format',
         '- Send `epub pdf` to download both epub and pdf formats.',
         '- Send `{space separated format names}` for multiple formats',
         'Available formats: `' + '` `'.join(available_formats) + '`']))
        self.state = self.handle_output_selection

    def handle_output_selection--- This code section failed: ---

 L. 447         0  LOAD_FAST                'self'
                2  LOAD_ATTR                busy_state
                4  LOAD_FAST                'self'
                6  STORE_ATTR               state

 L. 449         8  LOAD_FAST                'self'
               10  LOAD_ATTR                message
               12  LOAD_ATTR                content
               14  LOAD_METHOD              strip
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'text'

 L. 450        20  LOAD_FAST                'text'
               22  LOAD_METHOD              startswith
               24  LOAD_STR                 '!cancel'
               26  CALL_METHOD_1         1  ''
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L. 451        30  LOAD_FAST                'self'
               32  LOAD_METHOD              get_novel_url
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          

 L. 452        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            28  '28'

 L. 455        42  LOAD_GLOBAL              set
               44  LOAD_GLOBAL              re
               46  LOAD_METHOD              findall
               48  LOAD_STR                 '|'
               50  LOAD_METHOD              join
               52  LOAD_GLOBAL              available_formats
               54  CALL_METHOD_1         1  ''
               56  LOAD_FAST                'text'
               58  LOAD_METHOD              lower
               60  CALL_METHOD_0         0  ''
               62  CALL_METHOD_2         2  ''
               64  CALL_FUNCTION_1       1  ''
               66  STORE_DEREF              'output_format'

 L. 456        68  LOAD_GLOBAL              len
               70  LOAD_DEREF               'output_format'
               72  CALL_FUNCTION_1       1  ''
               74  POP_JUMP_IF_TRUE    108  'to 108'

 L. 457        76  LOAD_GLOBAL              set
               78  LOAD_GLOBAL              available_formats
               80  CALL_FUNCTION_1       1  ''
               82  STORE_DEREF              'output_format'

 L. 458        84  LOAD_FAST                'self'
               86  LOAD_METHOD              send_sync
               88  LOAD_STR                 'Sorry! I did not recognize your input. '

 L. 459        90  LOAD_STR                 'By default, I shall generate in (%s) formats.'
               92  LOAD_STR                 ', '
               94  LOAD_METHOD              join
               96  LOAD_DEREF               'output_format'
               98  CALL_METHOD_1         1  ''
              100  BINARY_MODULO    

 L. 458       102  BINARY_ADD       
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
            108_0  COME_FROM            74  '74'

 L. 462       108  LOAD_CLOSURE             'output_format'
              110  BUILD_TUPLE_1         1 
              112  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              114  LOAD_STR                 'MessageHandler.handle_output_selection.<locals>.<dictcomp>'
              116  MAKE_FUNCTION_8          'closure'
              118  LOAD_GLOBAL              available_formats
              120  GET_ITER         
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                app
              128  STORE_ATTR               output_formats

 L. 463       130  LOAD_FAST                'self'
              132  LOAD_METHOD              send_sync
              134  LOAD_STR                 'I will generate e-book in (%s) format'
              136  LOAD_STR                 ', '
              138  LOAD_METHOD              join
              140  LOAD_DEREF               'output_format'
              142  CALL_METHOD_1         1  ''
              144  BINARY_MODULO    
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 465       150  LOAD_FAST                'self'
              152  LOAD_METHOD              send_sync
              154  LOAD_STR                 '\n'
              156  LOAD_METHOD              join

 L. 466       158  LOAD_STR                 'Starting download...'

 L. 467       160  LOAD_STR                 'Send anything to view status.'

 L. 468       162  LOAD_STR                 'Send `!cancel` to stop it.'

 L. 465       164  BUILD_LIST_3          3 
              166  CALL_METHOD_1         1  ''
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 471       172  LOAD_FAST                'self'
              174  LOAD_ATTR                executor
              176  LOAD_METHOD              submit
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                start_download
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 112

    def start_download(self):
        self.app.pack_by_volume = False
        try:
            try:
                self.send_sync('**%s**' % self.app.crawler.novel_title, 'Downloading %d chapters...' % len(self.app.chapters))
                self.app.start_download()
                self.send_sync('Download complete.')
                self.send_sync('Binding books...')
                self.app.bind_books()
                self.send_sync('Book binding completed.')
                self.send_sync('Compressing output folder...')
                self.app.compress_books()
                self.send_sync('Compressed output folder.')
                if public_ip and public_path and os.path.exists(public_path):
                    self.send_sync('Publishing files...')
                    self.publish_files()
                else:
                    self.send_sync('Uploading files...')
                    for archive in self.app.archived_outputs:
                        self.upload_file(archive)

            except Exception as ex:
                try:
                    logger.exception('Failed to download')
                    self.send_sync('Download failed!\n`%s`' % str(ex))
                    self.executor.submit(self.destroy)
                finally:
                    ex = None
                    del ex

        finally:
            self.executor.submit(self.destroy)

    def publish_files(self):
        try:
            download_url = '%s/%s/%s' % (public_ip.strip('/'),
             quote(str(self.user.id)),
             quote(os.path.basename(self.app.output_path)))
            self.send_sync('Download files from:\n' + download_url)
        except Exception:
            logger.exception('Fail to publish')

    def upload_file(self, archive):
        file_size = os.stat(archive).st_size
        if file_size > 8378122.24:
            self.send_sync('File %s exceeds 8MB. Uploading To Google Drive.' % os.path.basename(archive))
            description = 'Generated By : Discord Bot Ebook Smelter'
            link_id = upload(archive, description)
            if link_id:
                self.send_sync('https://drive.google.com/open?id=%s' % link_id)
            else:
                self.send_sync('Failed to upload to google drive')
        else:
            k = 0
            while file_size > 1024:
                if k < 3:
                    k += 1
                    file_size /= 1024.0

            self.send_sync('Uploading %s [%d%s] ...' % (
             os.path.basename(archive),
             int(file_size * 100) / 100.0,
             [
              'B', 'KB', 'MB', 'GB'][k]))
            self.wait_for(self.user.send(file=(discord.File(open(archive, 'rb'), os.path.basename(archive)))))