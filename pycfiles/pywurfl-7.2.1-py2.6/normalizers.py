# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywurfl/algorithms/wurfl/normalizers.py
# Compiled at: 2011-01-06 14:56:36
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
import re
babel_fish_re = re.compile('\\s*\\(via babelfish.yahoo.com\\)\\s*', re.UNICODE)
uplink_re = re.compile('\\s*UP\\.Link.+$', re.UNICODE)
yeswap_re = re.compile('\\s*Mozilla/4\\.0 \\(YesWAP mobile phone proxy\\)', re.UNICODE)
safari_re = re.compile('(Mozilla\\/5\\.0.*)(\\;\\s*U\\;.*?)(Safari\\/\\d{0,3})', re.UNICODE)
locale_re = re.compile('(; [a-z]{2}(-[a-zA-Z]{0,2})?)', re.UNICODE)
serial_number_re = re.compile('(\\[(TF|NT|ST)[\\d|X]+\\])|(\\/SN[\\d|X]+)', re.UNICODE)
android_re = re.compile('(Android[\\s/]\\d.\\d)(.*?;)', re.UNICODE)
konqueror_re = re.compile('(Konqueror\\/\\d)', re.UNICODE)

def babelfish(user_agent):
    """Replace the "via babelfish.yahoo.com" with ''"""
    return babel_fish_re.sub('', user_agent)


def blackberry(user_agent):
    """ Replaces the heading "BlackBerry" string with ''"""
    try:
        index = user_agent.index('BlackBerry')
        if 'AppleWebKit' not in user_agent:
            return user_agent[index:]
    except ValueError:
        pass

    return user_agent


def uplink(user_agent):
    """Replace the trailing UP.Link ... with ''"""
    return uplink_re.sub('', user_agent)


def yeswap(user_agent):
    """Replace the "YesWAP mobile phone proxy" with ''"""
    return yeswap_re.sub('', user_agent)


def locale_remover(user_agent):
    return locale_re.sub('', user_agent, 1)


def serial_no(user_agent):
    return serial_number_re.sub('', user_agent, 1)


def _combine_funcs(*funcs):

    def normalizer(user_agent):
        for f in funcs:
            user_agent = f(user_agent)

        return user_agent.replace('  ', ' ').strip()

    return normalizer


generic = _combine_funcs(serial_no, blackberry, uplink, yeswap, babelfish, locale_remover)

def prenormalized(normalizer_func):

    def combined_normalizer(user_agent):
        user_agent = generic(user_agent)
        return normalizer_func(user_agent)

    combined_normalizer.__doc__ = normalizer_func.__doc__
    return combined_normalizer


def _specific_normalizer(user_agent, search_string, vsn_size):
    if search_string in user_agent:
        start = user_agent.index(search_string)
        user_agent = user_agent[start:start + vsn_size]
    return user_agent


@prenormalized
def chrome(user_agent):
    return _specific_normalizer(user_agent, 'Chrome', 8)


@prenormalized
def firefox(user_agent):
    return _specific_normalizer(user_agent, 'Firefox', 11)


@prenormalized
def konqueror(user_agent):
    match = konqueror_re.search(user_agent)
    if match:
        user_agent = match.group(1)
    return user_agent


@prenormalized
def msie(user_agent):
    if 'MSIE' in user_agent:
        user_agent = user_agent[0:user_agent.index('MSIE') + 9]
    return user_agent


@prenormalized
def safari(user_agent):
    """
    Return the safari user agent stripping out all the characters between
    U; and Safari/xxx

    e.g Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; fr) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.1 Safari/525.18
    becomes
    Mozilla/5.0 (Macintosh Safari/525
    """
    match = safari_re.search(user_agent)
    if match and len(match.groups()) >= 3:
        user_agent = (' ').join([match.group(1).strip(), match.group(3).strip()])
    return user_agent


@prenormalized
def lg(user_agent):
    try:
        lg_index = user_agent.index('LG')
        return user_agent[lg_index:]
    except ValueError:
        return user_agent


@prenormalized
def maemo(user_agent):
    try:
        maemo_index = user_agent.index('Maemo')
        return user_agent[maemo_index:]
    except ValueError:
        return user_agent


@prenormalized
def android(user_agent):
    match = android_re.search(user_agent)
    if match:
        user_agent = android_re.sub(match.group(1) + ';', user_agent)
    return user_agent