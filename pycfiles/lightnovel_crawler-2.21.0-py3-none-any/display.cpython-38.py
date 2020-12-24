# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\core\display.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 5336 bytes
import logging, os, textwrap
from urllib.parse import urlparse
from colorama import Back, Fore, Style
from assets.icons import Icons
from ..sources import crawler_list
LINE_SIZE = 80
try:
    row, _ = os.get_terminal_size()
    if row < LINE_SIZE:
        LINE_SIZE = row
except Exception:
    pass
else:

    def description():
        print('=' * LINE_SIZE)
        title = Icons.BOOK + ' Lightnovel Crawler ' + Icons.CLOVER + os.getenv('version')
        padding = ' ' * ((LINE_SIZE - len(title)) // 2)
        print(Fore.YELLOW, padding + title, Fore.RESET)
        desc = 'https://github.com/dipu-bd/lightnovel-crawler'
        padding = ' ' * ((LINE_SIZE - len(desc)) // 2)
        print(Style.DIM, padding + desc, Style.RESET_ALL)
        print('-' * LINE_SIZE)


    def epilog():
        print()
        print('-' * LINE_SIZE)
        print(' ' + Icons.LINK, Fore.CYAN, 'https://github.com/dipu-bd/lightnovel-crawler/issues', Fore.RESET)
        print('=' * LINE_SIZE)


    def debug_mode(level):
        text = Fore.RED + ' ' + Icons.SOUND + ' '
        text += 'LOG LEVEL: %s' % level
        text += Fore.RESET
        padding = ' ' * ((LINE_SIZE - len(text)) // 2)
        print(padding + text)
        print('-' * LINE_SIZE)


    def input_suppression():
        text = Fore.RED + ' ' + Icons.ERROR + ' '
        text += 'Input is suppressed'
        text += Fore.RESET
        print(text)
        print('-' * LINE_SIZE)


    def cancel_method():
        print()
        print(Icons.RIGHT_ARROW, 'Press', Fore.MAGENTA, 'Ctrl + C', Fore.RESET, 'to exit')
        print()


    def error_message(err):
        print()
        print(Fore.RED, Icons.ERROR, 'Error:', err, Fore.RESET)
        print()


    def app_complete():
        print(Style.BRIGHT + Fore.YELLOW + Icons.SPARKLE, 'Task completed', Fore.RESET, Style.RESET_ALL)
        print()


    def new_version_news(latest):
        print('', Icons.PARTY + Style.BRIGHT + Fore.CYAN, 'VERSION', Fore.RED + latest + Fore.CYAN, 'IS NOW AVAILABLE!', Fore.RESET)
        print('', Icons.RIGHT_ARROW, Style.DIM + 'Upgrade:', Fore.YELLOW + 'pip install -U lightnovel-crawler', Style.RESET_ALL)
        if Icons.isWindows:
            print('', Icons.RIGHT_ARROW, Style.DIM + 'Download:', Fore.YELLOW + 'https://rebrand.ly/lncrawl', Style.RESET_ALL)
        else:
            if Icons.isLinux:
                print('', Icons.RIGHT_ARROW, Style.DIM + 'Download:', Fore.YELLOW + 'https://rebrand.ly/lncrawl-linux', Style.RESET_ALL)
        print('-' * LINE_SIZE)


    def url_supported_list():
        print('Supported sources:')
        for url in sorted(crawler_list.keys()):
            print(Fore.LIGHTGREEN_EX, Icons.RIGHT_ARROW, url, Fore.RESET)


    def url_not_recognized():
        print()
        print(Fore.RED, Icons.ERROR, 'Sorry! I do not recognize this website yet.', Fore.RESET)
        print()
        print('Find the list of supported/rejected sources here:')
        print(Fore.CYAN, Icons.LINK, 'https://github.com/dipu-bd/lightnovel-crawler#c3-supported-sources', Fore.RESET)
        print()
        print('You can request developers to add support for this site here:')
        print(Fore.CYAN, Icons.LINK, 'https://github.com/dipu-bd/lightnovel-crawler/issues', Fore.RESET)


    def url_rejected(reason):
        print()
        print(Fore.RED, Icons.ERROR, 'Sorry! I do not support this website.', Fore.RESET)
        print(Fore.RED, Icons.EMPTY, 'Reason:', reason, Fore.RESET)
        print()
        print('-' * LINE_SIZE)
        print('You can try other available sources or create an issue if you find something\nhas went wrong:')
        print(Fore.CYAN, Icons.LINK, 'https://github.com/dipu-bd/lightnovel-crawler/issues', Fore.RESET)


    def format_short_info_of_novel(short_info):
        if not short_info or len(short_info) == 0:
            return ''
        return '\n'.join(textwrap.wrap(short_info,
          width=70,
          initial_indent=('\n      ' + Icons.INFO),
          subsequent_indent='        ',
          drop_whitespace=True,
          break_long_words=True))


    def format_novel_choices(choices):
        items = []
        for index, item in enumerate(choices):
            text = '%d. %s [in %d sources]' % (
             index + 1, item['title'], len(item['novels']))
            if len(item['novels']) == 1:
                novel = item['novels'][0]
                short_info = novel['info'] if 'info' in novel else ''
                text += '\n      - ' + novel['url']
                text += format_short_info_of_novel(short_info)
            items.append({'name': text})
        else:
            return items


    def format_source_choices(novels):
        items = []
        for index, item in enumerate(novels):
            text = '%d. %s' % (index + 1, item['url'])
            short_info = item['info'] if 'info' in item else ''
            text += format_short_info_of_novel(short_info)
            items.append({'name': text})
        else:
            return items