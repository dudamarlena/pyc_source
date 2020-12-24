# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bfschott/Source/cmsplugin-newsplus/cmsplugin_newsplus/settings.py
# Compiled at: 2017-12-04 14:10:18
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _

def get_setting(name, default):
    """
    A little helper for fetching global settings with a common prefix.
    """
    parent_name = ('CMSPLUGIN_NEWS_{0}').format(name)
    return getattr(django_settings, parent_name, default)


DISABLE_LATEST_NEWS_PLUGIN = get_setting('DISABLE_LATEST_NEWS_PLUGIN', False)
FEED_SIZE = get_setting('FEED_SIZE', 10)
FEED_TITLE = get_setting('FEED_TITLE', _('News feed'))
FEED_DESCRIPTION = get_setting('FEED_DESCRIPTION', _('A feed full of news'))
ARCHIVE_PAGE_SIZE = get_setting('ARCHIVE_PAGE_SIZE', 15)
LINK_AS_ABSOLUTE_URL = get_setting('LINK_AS_ABSOLUTE_URL', True)
USE_LINK_ON_EMPTY_CONTENT_ONLY = get_setting('USE_LINK_ON_EMPTY_CONTENT_ONLY', True)
STATIC_URL = '/static/'