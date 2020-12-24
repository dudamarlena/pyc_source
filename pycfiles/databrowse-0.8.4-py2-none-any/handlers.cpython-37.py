# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\plugins\db_webpage_viewer\handlers.py
# Compiled at: 2018-06-29 17:51:46
# Size of source mod 2**32: 3199 bytes
""" plugins/handlers/dbh_html.py - Generic Web Page Handler """

def dbh_html(path, contenttype, extension, roottag, nsurl):
    """ Generic Web Page Handler - Returns html_generic for Web Pages """
    if extension.lower() == 'html' or extension.lower() == 'htm':
        return 'db_webpage_viewer'
    return False