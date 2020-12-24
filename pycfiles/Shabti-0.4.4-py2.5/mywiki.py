# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/config/wikifarm/mywiki.py
# Compiled at: 2010-04-25 11:53:22
"""
This is a sample config for a wiki that is part of a wiki farm and uses
farmconfig for common stuff. Here we define what has to be different from
the farm's common settings.
"""
from farmconfig import FarmConfig

class Config(FarmConfig):
    sitename = 'MyWiki'
    interwikiname = 'MyWiki'
    page_front_page = 'FrontPage'
    data_dir = '/org/mywiki/data/'