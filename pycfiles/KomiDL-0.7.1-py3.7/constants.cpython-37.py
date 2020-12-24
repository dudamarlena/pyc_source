# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\constants.py
# Compiled at: 2019-10-12 01:27:51
# Size of source mod 2**32: 2807 bytes
"""This module contains constants used by KomiDL"""
VERSION = '0.7.1'
STATUSBAR_LEN = 65
USER_AGENT = 'komidl/0.1'
ARCHIVE_FORMATS = {
 'zip', 'tar', 'gztar', 'bztar'}
IMAGE_FORMATS = {
 'jpg', 'png', 'jpeg', 'tiff', 'bmp', 'webp', 'svg'}
COMMON_FORMATS = ('jpg', 'png', 'gif', 'gifv', 'jpeg', 'tiff', 'bmp', 'webp', 'svg')
LANG_TO_ISO = {'Japanese':'JA', 
 'English':'EN',  'Chinese':'ZH',  'French':'FR', 
 'Spanish':'ES',  'Korean':'KR',  'German':'DE',  'Russian':'RU', 
 'Italian':'IT',  'Portuguese':'PT'}
ISO_LANG_SET = {'ja':('ja', 'jp', 'jap'), 
 'en':('en', 'eng', 'us', 'gb'),  'zh':('zh', 'cn'), 
 'es':('es', 'mx', 'sp'),  'de':('de', 'ger'), 
 'ru':('ru', 'rus'),  'pt':('pt', 'br')}
KOMIDL_LOGO = '   +++++++++++++++++++++++++++++   \n +++:-------------------------:+++ \n+++`.//+++++++++++++++++++++//.`+++\n++/`+/          `+`          /+`/++\n++/`++::::::::- `+:::::::::::++`/++\n++/`++++++++++: `+.          /+`/++\n++/`++////////- `+:----------++`/++\n++/`+/          `+.          /+`/++\n++/`++:::::::::::+:::////////++`/++\n++/`+/          `+` :++++++++++`/++\n++/`++--//////- `+` :++++++++++`/++\n++/`+/  /+++++: `+` :++++++++++`/++\n++/`+/  ::::::- `+` -::::::::++`/++\n++/`+/          `+`          /+`/++\n+++`./+++++++++++++++++++++++/.`+++\n +++:-------------------------:+++ \n   +++++++++++++++++++++++++++++   '