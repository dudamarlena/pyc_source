# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/django-ninecms/ninecms/settings.py
# Compiled at: 2016-04-06 06:07:34
# Size of source mod 2**32: 7702 bytes
""" Settings default definition for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
SITE_NAME = '9cms'
SITE_AUTHOR = '9cms'
SITE_KEYWORDS = ''
IMAGE_STYLES = {'thumbnail': {'type': 'thumbnail', 
               'size': (
                        150, 1000)}, 
 'thumbnail_crop': {'type': 'thumbnail-crop', 
                    'size': (
                             150, 150)}, 
 'thumbnail_upscale': {'type': 'thumbnail-upscale', 
                       'size': (
                                150, 150)}, 
 'gallery_style': {'type': 'thumbnail', 
                   'size': (
                            400, 1000)}, 
 'blog_style': {'type': 'thumbnail-crop', 
                'size': (
                         350, 226)}, 
 'large': {'type': 'thumbnail', 
           'size': (
                    1280, 1280)}}
TRANSLITERATE_REMOVE = '"\'`,:;|{[}]+=*&%^$#@!~()?<>'
TRANSLITERATE_REPLACE = (
 ' .-_/', '-----')
LANGUAGE_MENU_LABELS = 'name'
I18N_URLS = True