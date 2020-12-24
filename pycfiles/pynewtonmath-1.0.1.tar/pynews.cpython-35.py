# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/pynews/pynews.py
# Compiled at: 2016-10-22 01:48:25
# Size of source mod 2**32: 2867 bytes
__doc__ = 'Script to gather news from HackerNews.'
import argparse, multiprocessing, sys, requests as req
from .utils import get_stories, create_list_stories, create_menu
DEFAULT_THREADS_NUMBER = multiprocessing.cpu_count()

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(prog='PyNews-CLI', description="Your news collector inside your terminal! Tell me, what's                      cooler than that?", usage='\n        PyNews-CLI - News Collector from HackerNews API\n        Usage: pynews [-t/--top-stories number_of_stories]\n                      [-n/--news-stories number_of_stories]\n\n        If the number of stories is not supplied, will be showed 200 from the\n        500 stories.\n\n        Examples:\n        - Get Top Stories:\n            $ pynews -t 10 # or\n            $ pynews --top-stories 10\n            This will show the 10 first top stories from the list of 500.\n\n        - Get New Stories:\n            $ pynews -n 10 # or\n            $ pynews --news-stories\n            This will show the 10 first new stories from the list of 500.\n\n        Get basic options and Help, use: -h\\--help\n\n        ')
    parser.add_argument('-t', '--top-stories', nargs='?', const=200, type=int, help='Get the top N stories from HackerNews API')
    parser.add_argument('-n', '--news-stories', nargs='?', const=200, type=int, help='Get the N new stories from HackerNews API')
    parser.add_argument('-s', '--shuffle', nargs='?', const=False, type=bool, help='Get the N new stories from HackerNews API')
    parser.add_argument('-T', '--threads', nargs='?', const=DEFAULT_THREADS_NUMBER, type=int, help='Determine the number max of threads')
    options = parser.parse_args()
    if options.top_stories:
        param = (
         options.top_stories, 'top')
    else:
        param = (
         options.news_stories, 'news')
    list_data = None
    try:
        list_data = get_stories(param[1])
    except req.ConnectionError:
        print('A connection problem occurred.')
    except req.Timeout:
        print('A timeout problem occurred.')
    except req.TooManyRedirects:
        print('The request exceeds the configured number            of maximum redirections.')

    if not list_data:
        return
    max_threads = options.threads if options.threads or 0 > 0 else DEFAULT_THREADS_NUMBER
    list_dict_stories = create_list_stories(list_data, param[0], options.shuffle, max_threads)
    menu = create_menu(list_dict_stories, param[1])
    menu.show()


if __name__ == '__main__':
    sys.exit(main())