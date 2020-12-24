# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\httphelp\content_generator.py
# Compiled at: 2018-11-27 06:45:48
# Size of source mod 2**32: 2131 bytes
import sys, yaml, urwid
from httphelp.constants import CURR_DIR
from httphelp.app_handler import Scrollable

def __load_file_data(num):
    copyleft = yaml.safe_load(open('/'.join([CURR_DIR, 'copyright_description.yml']), 'r'))
    if num:
        return copyleft['statuscode']
    return copyleft['headers']


def generate_content(status_code):
    try:
        code_descriptions, num, status_code = get_yaml_dictionary(status_code)
        content = code_descriptions[status_code]
        pile = urwid.Pile([
         urwid.Text('HTTPHELP: The Manual for HTTP Status Codes and Headers\n', align='center'),
         urwid.Text(('title', 'STATUS MESSAGE' if num else 'HEADER INFO')),
         urwid.Padding((urwid.Text(''.join([str(status_code), ': ' if num else ', Example= ', content['message'], '\n']))),
           left=5),
         urwid.Text(('title', 'CATEGORY')),
         urwid.Padding((urwid.Text(''.join([content['category'], '\n']))), left=5),
         urwid.Text(('title', 'DESCRIPTION')),
         urwid.Padding((urwid.Text(''.join([content['description'], '\n']))), left=5),
         urwid.Text(('title', 'COPYRIGHT')),
         urwid.Padding((urwid.Text(''.join([__load_file_data(num), '\n']))), left=5)])
        padding = urwid.Padding((Scrollable(pile)), left=1, right=1)
        return padding
    except KeyError:
        return


def get_yaml_dictionary(status_code):
    try:
        status_code = int(status_code)
        num = True
        filename = 'code_descriptions.yml'
    except (TypeError, ValueError):
        num = False
        filename = 'header_descriptions.yml'

    try:
        code_descriptions = yaml.safe_load(open('/'.join([CURR_DIR, filename]), 'r'))
    except yaml.constructor.ConstructorError:
        print('Invalid file. Only support valid json and yaml files.')
        sys.exit(1)

    return (code_descriptions, num, status_code)