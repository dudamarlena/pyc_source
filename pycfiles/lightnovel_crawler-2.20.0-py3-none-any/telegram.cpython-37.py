# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\telegram.py
# Compiled at: 2019-11-15 01:18:07
# Size of source mod 2**32: 25741 bytes
import logging, os, re, shutil
from urllib.parse import urlparse
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, Filters, Handler, MessageHandler, RegexHandler, Updater
from ..binders import available_formats
from core.app import App
from ..spiders import crawler_list
from utils.uploader import upload
logger = logging.getLogger('TELEGRAM_BOT')

class TelegramBot:

    def start(self):
        self.updater = Updater(os.getenv('TELEGRAM_TOKEN', ''))
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('help', self.show_help))
        conv_handler = ConversationHandler(entry_points=[
         CommandHandler('start', (self.init_app), pass_user_data=True),
         MessageHandler((Filters.text),
           (self.handle_novel_url), pass_user_data=True)],
          fallbacks=[
         CommandHandler('cancel', (self.destroy_app), pass_user_data=True)],
          states={'handle_novel_url':[
          MessageHandler((Filters.text),
            (self.handle_novel_url), pass_user_data=True)], 
         'handle_crawler_to_search':[
          CommandHandler('skip',
            (self.handle_crawler_to_search), pass_user_data=True),
          MessageHandler((Filters.text),
            (self.handle_crawler_to_search), pass_user_data=True)], 
         'handle_select_novel':[
          MessageHandler((Filters.text),
            (self.handle_select_novel), pass_user_data=True)], 
         'handle_select_source':[
          MessageHandler((Filters.text),
            (self.handle_select_source), pass_user_data=True)], 
         'handle_delete_cache':[
          MessageHandler((Filters.text),
            (self.handle_delete_cache), pass_user_data=True)], 
         'handle_range_selection':[
          CommandHandler('all', (self.handle_range_all), pass_user_data=True),
          CommandHandler('last', (self.handle_range_last), pass_user_data=True),
          CommandHandler('first',
            (self.handle_range_first), pass_user_data=True),
          CommandHandler('volume',
            (self.handle_range_volume), pass_user_data=True),
          CommandHandler('chapter',
            (self.handle_range_chapter), pass_user_data=True),
          MessageHandler(Filters.text, self.display_range_selection_help)], 
         'handle_volume_selection':[
          MessageHandler((Filters.text),
            (self.handle_volume_selection), pass_user_data=True)], 
         'handle_chapter_selection':[
          MessageHandler((Filters.text),
            (self.handle_chapter_selection), pass_user_data=True)], 
         'handle_pack_by_volume':[
          MessageHandler((Filters.text),
            (self.handle_pack_by_volume), pass_user_data=True)], 
         'handle_output_format':[
          MessageHandler((Filters.text),
            (self.handle_output_format), pass_job_queue=True, pass_user_data=True)]})
        dp.add_handler(conv_handler)
        dp.add_handler(MessageHandler((Filters.text),
          (self.handle_downloader), pass_user_data=True))
        dp.add_error_handler(self.error_handler)
        self.updater.start_polling()
        print('Telegram bot is online!')
        self.updater.idle()

    def error_handler(self, bot, update, error):
        """Log Errors caused by Updates."""
        logger.warn('Error: %s\nCaused by: %s', error, update)

    def show_help(self, bot, update):
        update.message.reply_text('Send /start to create new session.\n')
        return ConversationHandler.END

    def destroy_app(self, bot, update, user_data):
        if user_data.get('job'):
            user_data.pop('job').schedule_removal()
        if user_data.get('app'):
            app = user_data.pop('app')
            app.destroy()
        update.message.reply_text('Session closed',
          reply_markup=(ReplyKeyboardRemove()))
        return ConversationHandler.END

    def init_app(self, bot, update, user_data):
        if user_data.get('app'):
            self.destroy_app(bot, update, user_data)
        app = App()
        app.initialize()
        user_data['app'] = app
        update.message.reply_text('A new session is created.')
        update.message.reply_text('I recognize input of these two categories:\n- Profile page url of a lightnovel.\n- A query to search your lightnovel.\nEnter whatever you want or send /cancel to stop.')
        return 'handle_novel_url'

    def handle_novel_url(self, bot, update, user_data):
        if user_data.get('job'):
            app = user_data.get('app')
            job = user_data.get('job')
            update.message.reply_text('%s\n%d out of %d chapters has been downloaded.\nTo terminate this session send /cancel.' % (
             user_data.get('status'), app.progress, len(app.chapters)))
        else:
            if user_data.get('app'):
                app = user_data.get('app')
            else:
                app = App()
                app.initialize()
                user_data['app'] = app
            app.user_input = update.message.text.strip()
            try:
                app.init_search()
            except Exception:
                update.message.reply_text('Sorry! I only recognize these sources:\nhttps://github.com/dipu-bd/lightnovel-crawler#c3-supported-sources')
                update.message.reply_text('Enter something again or send /cancel to stop.')
                return 'handle_novel_url'
            else:
                if app.crawler:
                    update.message.reply_text('Got your page link')
                    return self.get_novel_info(bot, update, user_data)
                if len(app.user_input) < 5:
                    update.message.reply_text('Please enter a longer query text (at least 5 letters).')
                    return 'handle_novel_url'
                update.message.reply_text('Got your query text')
                return self.show_crawlers_to_search(bot, update, user_data)

    def show_crawlers_to_search(self, bot, update, user_data):
        app = user_data.get('app')
        buttons = []

        def make_button(i, url):
            return '%d - %s' % (i + 1, urlparse(url).hostname)

        for i in range(1, len(app.crawler_links) + 1, 2):
            buttons += [
             [
              make_button(i - 1, app.crawler_links[(i - 1)]),
              make_button(i, app.crawler_links[i]) if i < len(app.crawler_links) else '']]

        update.message.reply_text('Choose where to search for your novel, \nor send /skip to search everywhere.',
          reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
        return 'handle_crawler_to_search'

    def handle_crawler_to_search(self, bot, update, user_data):
        app = user_data.get('app')
        link = update.message.text
        if link:
            selected_crawlers = []
            if link.isdigit():
                selected_crawlers += [
                 app.crawler_links[(int(link) - 1)]]
            else:
                selected_crawlers += [x for i, x in enumerate(app.crawler_links) if '%d - %s' % (i + 1, urlparse(x).hostname) == link]
            if len(selected_crawlers) != 0:
                app.crawler_links = selected_crawlers
        update.message.reply_text(('Searching for "%s" in %d sites. Please wait.' % (
         app.user_input, len(app.crawler_links))),
          reply_markup=(ReplyKeyboardRemove()))
        update.message.reply_text('DO NOT type anything until I reply.\nYou can only send /cancel to stop this session.')
        app.search_novel()
        return self.show_novel_selection(bot, update, user_data)

    def show_novel_selection(self, bot, update, user_data):
        app = user_data.get('app')
        if len(app.search_results) == 0:
            update.message.reply_text('No results found by your query.\nTry again or send /cancel to stop.')
            return 'handle_novel_url'
        if len(app.search_results) == 1:
            user_data['selected'] = app.search_results[0]
            return self.show_source_selection(bot, update, user_data)
        update.message.reply_text('Choose any one of the following novels, or send /cancel to stop this session.',
          reply_markup=ReplyKeyboardMarkup([['%d. %s (in %d sources)' % (index + 1, res['title'], len(res['novels']))] for index, res in enumerate(app.search_results)],
          one_time_keyboard=True))
        return 'handle_select_novel'

    def handle_select_novel(self, bot, update, user_data):
        app = user_data.get('app')
        selected = None
        text = update.message.text
        if text:
            if text.isdigit():
                selected = app.search_results[(int(text) - 1)]
            else:
                for i, item in enumerate(app.search_results[:10]):
                    sample = '%d. %s' % (i + 1, item['title'])
                    if text.startswith(sample):
                        selected = item
                    else:
                        if len(text) >= 5:
                            if text.lower() in item['title'].lower():
                                selected = item
                            else:
                                continue
                        break

        else:
            return selected or self.show_novel_selection(bot, update, user_data)
        user_data['selected'] = selected
        return self.show_source_selection(bot, update, user_data)

    def show_source_selection(self, bot, update, user_data):
        app = user_data.get('app')
        selected = user_data.get('selected')
        if len(selected['novels']) == 1:
            app.init_crawler(selected['novels'][0]['url'])
            return self.get_novel_info(bot, update, user_data)
        update.message.reply_text(('Choose a source to download "%s", ' % selected['title'] + 'or send /cancel to stop this session.'),
          reply_markup=ReplyKeyboardMarkup([['%d. %s %s' % (index + 1, novel['url'], novel['info'] if 'info' in novel else '')] for index, novel in enumerate(selected['novels'])],
          one_time_keyboard=True))
        return 'handle_select_source'

    def handle_select_source(self, bot, update, user_data):
        app = user_data.get('app')
        selected = user_data.get('selected')
        source = None
        text = update.message.text
        if text:
            if text.isdigit():
                source = selected['novels'][(int(text) - 1)]
            else:
                for i, item in enumerate(selected['novels']):
                    sample = '%d. %s' % (i + 1, item['url'])
                    if text.startswith(sample):
                        source = item
                    else:
                        if len(text) >= 5:
                            if text.lower() in item['url'].lower():
                                source = item
                            else:
                                continue
                        break

        else:
            return selected or self.show_source_selection(bot, update, user_data)
        app.init_crawler(source['url'])
        return self.get_novel_info(bot, update, user_data)

    def get_novel_info(self, bot, update, user_data):
        app = user_data.get('app')
        user = update.message.from_user
        update.message.reply_text(app.crawler.novel_url)
        update.message.reply_text('Reading novel info...')
        app.get_novel_info()
        if os.path.exists(app.output_path):
            update.message.reply_text('Local cache found do you want to use it',
              reply_markup=ReplyKeyboardMarkup([
             [
              'Yes', 'No']],
              one_time_keyboard=True))
            return 'handle_delete_cache'
        os.makedirs((app.output_path), exist_ok=True)
        update.message.reply_text(('%d volumes and %d chapters found.' % (
         len(app.crawler.volumes),
         len(app.crawler.chapters))),
          reply_markup=(ReplyKeyboardRemove()))
        return self.display_range_selection_help(bot, update)

    def handle_delete_cache(self, bot, update, user_data):
        app = user_data.get('app')
        user = update.message.from_user
        text = update.message.text
        if text.startswith('No'):
            if os.path.exists(app.output_path):
                shutil.rmtree((app.output_path), ignore_errors=True)
            os.makedirs((app.output_path), exist_ok=True)
        update.message.reply_text(('%d volumes and %d chapters found.' % (
         len(app.crawler.volumes),
         len(app.crawler.chapters))),
          reply_markup=(ReplyKeyboardRemove()))
        return self.display_range_selection_help(bot, update)

    def display_range_selection_help(self, bot, update):
        update.message.reply_text('\n'.join([
         'Send /all to download everything.',
         'Send /last to download last 50 chapters.',
         'Send /first to download first 50 chapters.',
         'Send /volume to choose specific volumes to download',
         'Send /chapter to choose a chapter range to download',
         'To tereminate this session, send /cancel.']))
        return 'handle_range_selection'

    def range_selection_done(self, bot, update, user_data):
        app = user_data.get('app')
        update.message.reply_text('You have selected %d chapters to download' % len(app.chapters))
        if len(app.chapters) == 0:
            return self.display_range_selection_help(bot, update)
        update.message.reply_text('Do you want to generate a single file or split the books into volumes?',
          reply_markup=ReplyKeyboardMarkup([
         [
          'Single file', 'Split by volumes']],
          one_time_keyboard=True))
        return 'handle_pack_by_volume'

    def handle_range_all(self, bot, update, user_data):
        app = user_data.get('app')
        app.chapters = app.crawler.chapters[:]
        return self.range_selection_done(bot, update, user_data)

    def handle_range_first(self, bot, update, user_data):
        app = user_data.get('app')
        app.chapters = app.crawler.chapters[:50]
        return self.range_selection_done(bot, update, user_data)

    def handle_range_last(self, bot, update, user_data):
        app = user_data.get('app')
        app.chapters = app.crawler.chapters[-50:]
        return self.range_selection_done(bot, update, user_data)

    def handle_range_volume(self, bot, update, user_data):
        app = user_data.get('app')
        buttons = [str(vol['id']) for vol in app.crawler.volumes]
        update.message.reply_text('I got these volumes: ' + ', '.join(buttons) + '\nEnter which one these volumes you want to download separated space or commas.')
        return 'handle_volume_selection'

    def handle_volume_selection(self, bot, update, user_data):
        app = user_data.get('app')
        text = update.message.text
        selected = re.findall('\\d+', text)
        update.message.reply_text('Got the volumes: ' + ', '.join(selected))
        selected = [int(x) for x in selected]
        app.chapters = [chap for chap in app.crawler.chapters if selected.count(chap['volume']) > 0]
        return self.range_selection_done(bot, update, user_data)

    def handle_range_chapter(self, bot, update, user_data):
        app = user_data.get('app')
        chapters = app.crawler.chapters
        update.message.reply_text('I got %s  chapters' % len(chapters) + '\nEnter which start and end chapter you want to generate separated space or comma.')
        return 'handle_chapter_selection'

    def handle_chapter_selection(self, bot, update, user_data):
        app = user_data.get('app')
        text = update.message.text
        selected = re.findall('\\d+', text)
        print(selected)
        if len(selected) != 2:
            update.message.reply_text('Sorry, I did not understand. Please try again')
            return 'handle_range_chapter'
        selected = [int(x) for x in selected]
        app.chapters = app.crawler.chapters[selected[0] - 1:selected[1]]
        update.message.reply_text('Got the start chapter : %s' % selected[0] + '\nThe end chapter : %s' % selected[1] + '\nTotal chapter chosen is %s' % len(app.chapters))
        return self.range_selection_done(bot, update, user_data)

    def handle_pack_by_volume(self, bot, update, user_data):
        app = user_data.get('app')
        text = update.message.text.lower()
        if text.startswith('split'):
            app.pack_by_volume = True
            update.message.reply_text('I will split output files into volumes')
        else:
            if text.startswith('single'):
                update.message.reply_text('I will generate single output files whenever possible')
            else:
                update.message.reply_text('Unknown selection')
                return 'range_selection_done'
        format_list = [
         [
          'Get all (might be slower)']]
        format_list += [available_formats[i:i + 2] for i in range(0, len(available_formats), 2)]
        update.message.reply_text('In which format you want me to generate your book?',
          reply_markup=ReplyKeyboardMarkup(format_list,
          one_time_keyboard=True))
        return 'handle_output_format'

    def handle_output_format(self, bot, update, job_queue, user_data):
        app = user_data.get('app')
        user = update.message.from_user
        text = update.message.text.lower()
        if not app.output_formats:
            app.output_formats = {x:False for x in available_formats}
        selected_formats = [app.output_formats and app.output_formats[x] for x in available_formats]
        finish_selection = False
        if text in available_formats:
            app.output_formats[text] = not app.output_formats[x]
            update.message.reply_text('I will generate (%s) formats' % ', '.join(selected_formats))
        else:
            if text.startswith('get all'):
                app.output_formats = None
                finish_selection = True
            else:
                if text.startswith('finish'):
                    app.output_formats = {x:x in app.output_formats and app.output_formats[x] for x in available_formats}
                    finish_selection = True
                else:
                    format_list = finish_selection or [
                     [
                      'Finish Selection']]
                    format_list += [available_formats[i:i + 2] for i in range(0, len(available_formats), 2)]
                    update.message.reply_text(reply_message,
                      reply_markup=ReplyKeyboardMarkup(format_list,
                      one_time_keyboard=True))
                    return 'handle_output_format'
                job = job_queue.run_once((self.process_download_request),
                  1,
                  context=(
                 update, user_data),
                  name=(str(user.id)))
                user_data['job'] = job
                update.message.reply_text(('Your request has been received.I will generate book in (%s) format' % ', '.join(selected_formats)),
                  reply_markup=(ReplyKeyboardRemove()))
                return ConversationHandler.END

    def process_download_request(self, bot, job):
        update, user_data = job.context
        app = user_data.get('app')
        if app:
            user_data['status'] = 'Downloading "%s"' % app.crawler.novel_title
            app.start_download()
            update.message.reply_text('Download finished.')
        app = user_data.get('app')
        if app:
            user_data['status'] = 'Generating output files'
            update.message.reply_text(user_data.get('status'))
            output_files = app.bind_books()
            update.message.reply_text('Output files generated.')
        app = user_data.get('app')
        if app:
            user_data['status'] = 'Compressing output folder.'
            update.message.reply_text(user_data.get('status'))
            app.compress_output()
        for archive in app.archived_outputs:
            link_id = upload(archive)
            if link_id:
                update.message.reply_text('Get your file here:https://drive.google.com/open?id=%s' % link_id)
            else:
                file_size = os.stat(archive).st_size
                if file_size < 52418314.24:
                    update.message.reply_document((open(archive, 'rb')),
                      timeout=86400)
                else:
                    update.message.reply_text('File size more than 50 MB so cannot be sent via telegram bot api check google drive link only')
            if os.path.exists(archive):
                os.remove(archive)
            update.message.reply_text('This file will be deleted on server')

        self.destroy_app(bot, update, user_data)

    def handle_downloader(self, bot, update, user_data):
        app = user_data.get('app')
        job = user_data.get('job')
        if app or job:
            update.message.reply_text('%s\n%d out of %d chapters has been downloaded.\nTo terminate this session send /cancel.' % (
             user_data.get('status'), app.progress, len(app.chapters)))
        return ConversationHandler.END