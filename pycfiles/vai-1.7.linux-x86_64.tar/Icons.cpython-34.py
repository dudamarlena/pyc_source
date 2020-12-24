# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/Icons.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 5137 bytes
from vaitk import gui
from pygments import token
import collections

class Icons:
    _ICONS = None

    @classmethod
    def getCollection(cls, collection_name):
        if cls._ICONS is None:
            cls._initIcons()
        return cls._ICONS[collection_name]

    @classmethod
    def _initIcons(cls):
        cls._ICONS = {}
        cls._ICONS['ascii'] = {'tabulator': '.', 
         'warning': 'W', 
         'error': 'E', 
         'info': 'I', 
         'added': '+', 
         'deletion_before': '_', 
         'deletion_after': '^', 
         'modified': '.', 
         'unexistent_line': '~', 
         'vertical_border': '|', 
         'bookmarks': 'abcdefghijklmnopqrstuvwxyz'}
        cls._ICONS['unicode1'] = {'tabulator': '╎', 
         'warning': '‼', 
         'error': '‼', 
         'info': 'I', 
         'added': '+', 
         'deletion_before': '⌄', 
         'deletion_after': '⌃', 
         'modified': '◾', 
         'unexistent_line': '~', 
         'vertical_border': '║', 
         'bookmarks': 'ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣ' + 'ⓤ' + 'ⓥ' + 'ⓦ' + 'ⓧ' + 'ⓨ' + 'ⓩ' + 'Ⓐ' + 'Ⓑ' + 'Ⓒ' + 'Ⓓ' + 'Ⓔ' + 'Ⓕ' + 'Ⓖ' + 'Ⓗ' + 'Ⓘ' + 'Ⓙ' + 'Ⓚ' + 'Ⓛ' + 'Ⓜ' + 'Ⓝ' + 'Ⓞ' + 'Ⓟ' + 'Ⓠ' + 'Ⓡ' + 'Ⓢ' + 'Ⓣ' + 'Ⓤ' + 'Ⓥ' + 'Ⓦ' + 'Ⓧ' + 'Ⓨ' + 'Ⓩ'}