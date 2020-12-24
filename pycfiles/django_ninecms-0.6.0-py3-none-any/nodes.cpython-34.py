# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/django-ninecms/ninecms/utils/nodes.py
# Compiled at: 2016-01-19 09:58:25
# Size of source mod 2**32: 1047 bytes
""" Node system utility functions """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.conf import settings

def get_full_path(path, language, bookmark=''):
    """ Utility function to build a valid path based on an initial
    :param path: the initial path
    :param language: language component
    :param bookmark: bookmark, if any
    :return: a valid path string
    """
    if not path.startswith('/'):
        path = '/' + path
    if not path.endswith('/'):
        path += '/'
    path += bookmark
    if language:
        if settings.I18N_URLS:
            path = '/' + language + path
    return path


def get_clean_url(url):
    """ Get a url without the language part, if i18n urls are defined
    :param url: a string with the url to clean
    :return: a string with the cleaned url
    """
    url = url.strip('/')
    url = '/' if not url else url
    if settings.I18N_URLS:
        return '/'.join(url.split('/')[1:])
    return url