# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seiran/onetab_bkm_import.py
# Compiled at: 2020-01-23 10:08:07
# Size of source mod 2**32: 1258 bytes
"""
Import bookmarks from the OneTab addon.
This is not extremely well-tested. Use at your own risk!
"""
import sqlite3, datetime, os, sys

def importFromTxt():
    """
    Import bookmarks from a plain-text list of titles and URLs.

    Returns
    -------
    onetab : list
        The bookmark data converted to Seiran's internal format.
    """
    onetab_file = input('Enter the path to the .txt exported from OneTab. > ')
    with open(onetab_file, 'r', encoding='utf-8') as (f):
        onetab_raw = f.read().splitlines()
    onetab = []
    for entry in onetab_raw:
        if not entry == '':
            if entry == '\n':
                pass
            else:
                entry_pieces = entry.split(' | ', 1)
                if len(entry_pieces) > 1:
                    title = entry_pieces[1]
                    url = entry_pieces[0]
                else:
                    title = entry_pieces[0]
                    url = entry_pieces[0]
                date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
                category = 'OneTab'
                bookmark = (title, url, date, category)
                onetab.append(bookmark)
        else:
            return onetab