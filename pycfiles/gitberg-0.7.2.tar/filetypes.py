# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/util/filetypes.py
# Compiled at: 2019-01-02 12:21:37
COMPRESSED_FILES = [
 '.zip', '.rar']
IGNORE_AUDIO_FILES = ['.m4b', '.ogg', '.spx', '.wav', '.raw', '.ogg~', '.mpg', '.mpeg', '.MP3', '.mp4', '.m4a', '.wma', '.aac']
AUDIO_FILES = ['mid', 'midi', 'sib', 'mus', 'mxl']
IMAGE_FILES = ['png', 'jpg', 'GIF', 'gif', 'bmp', 'tiff', 'tif', 'jpeg', 'JPG', 'eps', 'PNG']
MASTER_FILES = ['tei', 'rst', 'txt', 'rtf', 'tex', 'TXT']
MARKUP_FILES = ['htm', 'html', 'xml', 'eepic', 'css', 'xp', 'svg', 'ps', 'xsl']
GEN_FILES = [
 'pdf', 'ly', 'lit', 'prc', 'doc']
OTHER_KEEP_FILES = ['fen', 'ini']
IGNORE_FILES = IGNORE_AUDIO_FILES + COMPRESSED_FILES