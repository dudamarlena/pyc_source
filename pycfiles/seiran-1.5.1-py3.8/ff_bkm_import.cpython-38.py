# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seiran/ff_bkm_import.py
# Compiled at: 2020-01-23 10:08:07
# Size of source mod 2**32: 4132 bytes
"""
Import bookmarks from Firefox and derivatives (Pale Moon, IceCat, etc.)
This is not extremely well-tested. Use at your own risk!
"""
import sqlite3, datetime, os
from collections import OrderedDict

def formList(bookmark_tup):
    """
    Convert a tuple of bookmark data into a format Seiran can use.

    Parameters
    ----------
    bookmark_tup : tuple
        Raw bookmark data from the imported database.
    Returns
    -------
    conv_list : list
        The title, URL, and date for the bookmark.
    """
    title = bookmark_tup[0]
    url = bookmark_tup[1]
    date_raw = str(bookmark_tup[2])
    date_cut = date_raw[0:10]
    date = datetime.datetime.fromtimestamp(int(date_cut)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    conv_list = [title, url, date]
    return conv_list


def importDatabase():
    """
    Import a database from a Firefox-type browser.

    Returns
    -------
    fmarks : list
        The bookmark data converted to Seiran's internal format.
    """
    firefox = input('Please enter the directory of the Firefox profile you wish to import. > ')
    mobile = input("Is this from a mobile version of Firefox? If you're unsure, it probably is not. (y/n) > ")
    if mobile.lower() == 'y' or mobile.lower() == 'y':
        mobile = True
        database = os.path.join(firefox, 'browser.db')
    else:
        mobile = False
        database = os.path.join(firefox, 'places.sqlite')
    try:
        conn = sqlite3.connect(database)
    except sqlite3.OperationalError:
        print("Couldn't find a profile database of that type in {location}. You may be looking in the wrong directory, or it may be a different platform's database.".format(location=firefox))
    else:
        cursor = conn.cursor()
    if mobile == False:
        sql = 'select id,title from moz_bookmarks where type=2;'
        cursor.execute(sql)
        folders = cursor.fetchall()
        bookmarks = OrderedDict()
        for id in folders:
            bookmarks[id[1]] = cursor.execute("select b.title, a.url, b.dateAdded from moz_places a, moz_bookmarks b where a.id=b.fk and b.parent='%s';" % id[0]).fetchall()
        else:
            tup_list = []
            for i in bookmarks.items():
                tup_list.append(i)
            else:
                fmarks = []
                for i in tup_list:
                    folderName = i[0]
                    if folderName == '':
                        folderName == 'Blank'

                for item in i:
                    if i[1]:
                        bms = i[1]
                        for bookmark in bms:
                            bookmark_list = formList(bookmark)
                            bookmark_list.append(folderName)
                            fmarks.append(bookmark_list)
                        else:
                            continue

                else:
                    bookmarks = OrderedDict()
                    sql = 'select id,title from moz_bookmarks where type=1;'
                    cursor.execute(sql)
                    single_bookmarks = cursor.fetchall()
                    tup_list = []
                    single_bookmarks = single_bookmarks[0:20]
                    for id in single_bookmarks:
                        bookmarks[id[1]] = cursor.execute('select b.title, a.url, b.dateAdded from moz_places a, moz_bookmarks b where a.id=b.fk;').fetchall()
                    else:
                        for i in bookmarks.items():
                            tup_list.append(i)
                        else:
                            tup_list = tup_list[0][1]
                            for i in tup_list:
                                bookmark_list = formList(i)
                                bookmark_list.append('')
                                fmarks.append(bookmark_list)

    else:
        fmarks = []
        sql = 'select title,url,created from bookmarks;'
        bookmarks = cursor.execute(sql).fetchall()
        for i in bookmarks:
            bookmark_list = formList(i)
            bookmark_list.append('')
            fmarks.append(bookmark_list)
        else:
            conn.close()
            return fmarks