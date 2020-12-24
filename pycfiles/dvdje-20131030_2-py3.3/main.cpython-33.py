# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dvdje/main.py
# Compiled at: 2013-10-30 00:55:10
# Size of source mod 2**32: 5089 bytes
"""DV Dream Journal Exporter
Version 20131030-1 by Scott Garrett <mail@exovenom.net>

This script will save a copy of all dream journal entries from Dream Views in
their original BBCode formatting by reading entries from the journal editor.

"""
import codecs, getpass, logging, os, re, sys, textwrap, urllib.error
from . import htmlparser
from . import vbulletin
DV_URL = 'http://www.dreamviews.com'
DJ_PATH = 'blogs'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT, level='INFO')
logger = logging.getLogger(__name__)

def fat_safe_name(name):
    """Returns a FAT-friendly version of a file name."""
    name = name.replace('"', "'")
    name = name.replace('<', '{')
    name = name.replace('>', '}')
    name = re.sub('  +', ' ', name.strip())
    return re.sub('[^\\w ~!@#$%^&()_{},.=\\[\\]`-]', '-', name)


def main():
    print(__doc__)
    fn_date_fmt = '%Y-%m-%d %H%M'
    date_fmt = '%Y-%m-%d %H:%M'
    username = input('DV Username: ')
    username = username.strip()
    password = getpass.getpass('DV Password: ')
    add_titles = input('Add entry titles to filename [Y/n]? ')
    add_titles = False if add_titles.strip().lower() == 'n' else True
    save_directory = input('Save directory [DV Dream Journals]: ')
    save_directory = fat_safe_name(save_directory)
    if not save_directory:
        save_directory = 'DV Dream Journals'
    logger.info('Using save directory: %s', save_directory)
    dj_path = '{}/{}'.format(DJ_PATH, username)
    dv = vbulletin.Requests(DV_URL)
    edit_links = []
    logger.info('Logging in as %s', username)
    try:
        dv.login(username, password)
    except ValueError as error:
        logger.error('Failed to log in: %s', error)
        exit(1)

    logger.info('Logged in successfully')
    if not os.path.exists(save_directory):
        logger.info('Creating save directory: %s', save_directory)
        try:
            os.mkdir(save_directory)
        except (OSError, IOError) as error:
            logger.error('Failed to create directory: %s', error)
            exit(1)

    try:
        os.chdir(save_directory)
    except (OSError, IOError) as error:
        logger.error('Failed to change directory: %s', error)
        exit(1)

    while True:
        logger.info('Gathering up edit links from %s', dj_path)
        html = dv.html(dj_path)
        try:
            link_parser = htmlparser.EditEntryLinks()
            link_parser.feed(html)
            link_parser.close()
        except (ValueError, KeyError) as error:
            logger.error('Parsing failed: %s', error)
            exit(1)

        if not link_parser.urls:
            logger.error('No edit links were found in the journal browser.')
            exit(1)
        edit_links.extend(link_parser.urls)
        if link_parser.next_page_url is None:
            break
        dj_path = link_parser.next_page_url

    dj = htmlparser.DJParser()
    for link in edit_links:
        logger.info('Getting entry: %s', link)
        html = dv.html(link)
        logger.info('Parsing entry')
        dj.reset()
        dj.feed(html)
        dj.close()
        if dj.date is not None:
            fn_date = dj.date.strftime(fn_date_fmt)
            date = dj.date.strftime(date_fmt)
        else:
            date = '(unknown date)'
        filename = fn_date if not add_titles else ' - '.join((fn_date, dj.title))
        filename = fat_safe_name(filename) + '.txt'
        logger.info('Writing entry to disk: %s', filename)
        file_template = [
         'Date: ', date, '\n',
         'Title: ', dj.title, '\n',
         'Tags: ', ', '.join(dj.tags), '\n',
         '\n',
         dj.entry]
        try:
            with codecs.open(filename, 'w', 'utf-8') as (f):
                for part in file_template:
                    f.write(part)

                f.write('\n')
        except (OSError, IOError) as error:
            logger.error('Write failed: %s', error)
            exit(1)

        logger.info('Entry saved.')

    return


if __name__ == '__main__':
    try:
        main()
    except (urllib.error.URLError, urllib.error.HTTPError) as error:
        logger.error('Network error: %s', error)
        exit(1)
    except KeyboardInterrupt:
        logger.error('Aborted by user')
        exit(1)