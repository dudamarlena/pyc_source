# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywurfl/algorithms/wurfl/utils.py
# Compiled at: 2011-01-06 14:56:58
"""
This module contains the supporting classes for the Two Step Analysis user agent
algorithm that is used as the primary way to match user agents with the Java API
for the WURFL.

A description of the way the following source is intended to work can be found
within the source for the original Java API implementation here:
http://sourceforge.net/projects/wurfl/files/WURFL Java API/

The original Java code is GPLd and Copyright (c) WURFL-Pro srl
"""
__author__ = 'Armand Lynch <lyncha@users.sourceforge.net>'
__copyright__ = 'Copyright 2011, Armand Lynch'
__license__ = 'LGPL'
__url__ = 'http://celljam.net/'
__version__ = '1.2.1'
from functools import partial
mobile_browsers = [
 'cldc', 'symbian', 'midp', 'j2me', 'mobile',
 'wireless', 'palm', 'phone', 'pocket pc',
 'pocketpc', 'netfront', 'bolt', 'iris', 'brew',
 'openwave', 'windows ce', 'wap2', 'android',
 'opera mini', 'opera mobi', 'maemo', 'fennec',
 'blazer', '160x160', 'tablet', 'webos', 'sony',
 'nintendo', '480x640', 'aspen simulator',
 'up.browser', 'up.link', 'embider', 'danger hiptop',
 'obigo', 'foma']
desktop_browsers = [
 'slcc1', '.net clr', 'trident/4', 'media center pc',
 'funwebproducts', 'macintosh', 'wow64', 'aol 9.',
 'america online browser', 'googletoolbar']

def is_typeof_browser(user_agent, browsers=None):
    if browsers is None:
        return False
    else:
        user_agent = user_agent.lower()
        for b in browsers:
            if b in user_agent:
                return True

        return False


is_mobile_browser = partial(is_typeof_browser, browsers=mobile_browsers)
is_desktop_browser = partial(is_typeof_browser, browsers=desktop_browsers)

def ordinal_index(target, needle=' ', ordinal=1, start_index=0):
    index = -1
    working_target = target[start_index + 1:]
    if needle in working_target:
        i = 0
        for (i, x) in enumerate(working_target.split(needle)):
            if ordinal < 1:
                break
            index += len(x)
            ordinal -= 1

        index += i * len(needle) + start_index + 1
        index = index - (len(needle) - 1)
    if ordinal != 0:
        index = -1
    return index


def find_or_length(func, user_agent):
    value = func(user_agent)
    if value == -1:
        value = len(user_agent)
    return value


def indexof_or_length(target, needle=' ', position=1, start_index=0):
    value = ordinal_index(target, needle, position, start_index)
    if value == -1:
        value = len(target)
    return value


first_space = indexof_or_length
first_slash = partial(indexof_or_length, needle='/')
second_slash = partial(indexof_or_length, needle='/', position=2)
first_semi_colon = partial(indexof_or_length, needle=';')
third_space = partial(indexof_or_length, position=3)