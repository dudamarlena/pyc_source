# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/armor/validatorlib.py
# Compiled at: 2006-08-02 05:57:49
from re import match, sub
from string import ascii_letters, digits, punctuation

def min_len(minv):
    """ min_len(minv) -> returns function for checking string min len

    """

    def check(value):
        if len(value) >= minv:
            return value
        else:
            raise ValueError('Value too short')

    return check


def max_len(maxv):
    """ max_len(maxv) -> returns function for checking string max len

    """

    def check(value):
        if len(value) <= maxv:
            return value
        else:
            raise ValueError('Value too long')

    return check


def bound_len(minv, maxv):
    """ bound_len(minv, maxv) -> returns function for checking value length

    """
    minc = min_len(minv)
    maxc = max_len(maxv)

    def check(value):
        minc(value)
        maxc(value)
        return value

    return check


def all_not_in(seq):
    """ all_not_in(seq) -> returns function to ensure values are not in seq

    """

    def check(value):
        for token in seq:
            if token in value:
                raise ValueError('Value not safe')

        return value

    return check


def all_in(seq):
    """ all_in(seq) -> returns function to ensure values are in seq

    """

    def check(value):
        for token in value:
            if token not in seq:
                raise ValueError('Value not safe')

        return value

    return check


safe_sniff = all_not_in(list(punctuation))
alphanum_only = all_in(list(digits) + list(ascii_letters))

def is_formatted(pat):
    """ is_formatted(pat) -> returns function to ensure value matches pattern

    """

    def check(name):
        if match(pat, name):
            return name
        else:
            raise ValueError('Value does not match pattern')

    return check


host_pat = '^([a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.)*[a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?$'
smtp_pat = '^([a-zA-Z0-9_\\-\\.]+)@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.)|(([a-zA-Z0-9\\-]+\\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\\]?)$'
hostname_formatted = is_formatted(host_pat)
email_formatted = is_formatted(smtp_pat)

def html_escape(html):
    """ remove html entities from html

    """
    html = html.replace('&', '&amp;')
    html = html.replace('<', '&lt;')
    html = html.replace('>', '&gt;')
    html = html.replace('"', '&quot;')
    html = html.replace('(', '&#40;')
    html = html.replace(')', '&#41;')
    return html


def is_int(value):
    try:
        return int(value)
    except:
        raise ValueError('Not valid integer')