# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kapt/workspace/django-check-seo/django_check_seo/checks/site.py
# Compiled at: 2020-03-23 10:23:41
# Size of source mod 2**32: 1778 bytes
import re
from ..conf import settings

class Site:
    __doc__ = 'Structure containing a good amount of resources from the targeted webpage:\n    - the settings\n    - the soup (from beautifulsoup)\n    - the content (all html except header & menu)\n    - the full url\n    - the keywords\n    - the problems & warnings\n    '

    def __init__(self, soup, full_url):
        """Populate some vars.

        Arguments:
            soup {bs4.element} -- beautiful soup content (html)
            full_url {str} -- full url
        """
        self.settings = settings
        self.soup = soup
        self.content = self.soup.find_all('body')
        if settings.DJANGO_CHECK_SEO_EXCLUDE_CONTENT != '':
            for body in self.content:
                for node in body.select(settings.DJANGO_CHECK_SEO_EXCLUDE_CONTENT):
                    node.extract()

        self.content_text = ''
        for c in self.content:
            self.content_text += c.get_text(separator=' ')

        self.content_text = re.sub('(\\n( ?))+', '\n', self.content_text)
        self.content_text = re.sub('   +', '  ', self.content_text)
        self.full_url = full_url
        self.keywords = []
        self.problems = []
        self.warnings = []
        self.success = []