# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/config/wikifarm/farmconfig.py
# Compiled at: 2010-04-25 11:53:22
"""
    MoinMoin - Configuration for a wiki farm

    If you run a single wiki only, you can keep the "wikis" list "as is"
    (it has a single rule mapping all requests to mywiki.py).

    Note that there are more config options than you'll find in
    the version of this file that is installed by default; see
    the module MoinMoin.config.multiconfig for a full list of names and their
    default values.

    Also, the URL http://moinmo.in/HelpOnConfiguration has
    a list of config options.
"""
wikis = [
 ('mywiki', '.*')]
from MoinMoin.config import multiconfig, url_prefix_static

class FarmConfig(multiconfig.DefaultConfig):
    navi_bar = [
     'RecentChanges',
     'FindPage',
     'HelpContents']
    theme_default = 'modern'
    language_default = 'en'
    page_category_regex = '(?P<all>Category(?P<key>\\S+))'
    page_dict_regex = '(?P<all>(?P<key>\\S+)Dict)'
    page_group_regex = '(?P<all>(?P<key>\\S+)Group)'
    page_template_regex = '(?P<all>(?P<key>\\S+)Template)'
    show_hosts = 1
    show_interwiki = 1
    logo_string = ''