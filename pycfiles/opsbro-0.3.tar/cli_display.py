# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/opsbro-oss/opsbro/cli_display.py
# Compiled at: 2017-08-31 15:58:23
from opsbro.log import cprint, logger

def print_h1(title, raw_title=False, only_first_part=False, line_color='cyan', title_color='yellow'):
    p1 = 12
    l_title = len(title) - int(title.count('\x1b[') * 4.5)
    p2 = l_title + 2
    p3 = 80 - p1 - p2
    cprint('─' * p1, color=line_color, end='')
    if not raw_title:
        cprint(' %s ' % title, color=title_color, end='')
    else:
        cprint(' ' + title + ' ', end='')
    if not only_first_part:
        cprint('─' * p3, color=line_color)
    else:
        cprint('')


def print_h2(title, raw_title=False):
    cprint('᠁᠁᠁᠁᠁᠁᠁᠁᠁᠁᠁᠁', color='cyan', end='')
    if not raw_title:
        cprint(' %s ' % title, color='yellow')
    else:
        cprint(' ' + title + ' ')


def print_h3(title, raw_title=False):
    cprint('*', color='cyan', end='')
    if not raw_title:
        cprint(' %s ' % title, color='yellow')
    else:
        cprint(' ' + title + ' ')


def print_element_breadcumb(pack_name, pack_level, what, name=''):
    cprint('  * ', end='')
    cprint(pack_level, color='blue', end='')
    cprint(' > ', end='')
    cprint(pack_name, color='yellow', end='')
    cprint(' > ', end='')
    cprint(what, color='cyan', end='')
    if name:
        cprint(' > ', end='')
        cprint(name, color='magenta', end='')