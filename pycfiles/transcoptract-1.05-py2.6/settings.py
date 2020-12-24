# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv5tel/egg/transcoptract/settings.py
# Compiled at: 2011-09-27 16:07:17
HOST = 'localhost'
PORT = '9091'
FOLDER_IGNORE = 'sample|subs|proof'
FILENAME_IGNORE = '.*\\.nfo$|.*\\.sfv$|.*\\.idx$|.*\\.srt$|.*\\.torrent$|.*sample.*|.*sub\\.rar$'
RAR_FILE_MATCH = '.*\\.rar$|.*\\.[rs]\\d+$'
MAIN_RAR_FILE_MATCH = '(((?!\\.part\\d*.rar$).)*\\.rar$)|(.*\\.part0*1.rar$)'