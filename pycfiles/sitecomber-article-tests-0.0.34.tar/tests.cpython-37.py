# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nina/Documents/Sites/sitecomber-article-tests/sitecomber_article_tests/tests.py
# Compiled at: 2019-07-19 16:54:14
# Size of source mod 2**32: 3080 bytes
from sitecomber.apps.shared.interfaces import BaseSiteTest
from .utils import is_reader_view_enabled, contains_placeholder_text, get_article_readtime, check_spelling

def should_test_page(page):
    if not page.latest_request:
        return False
    else:
        if not page.is_internal:
            return False
        return page.latest_request.response or False
    if 'text/html' not in page.latest_request.response.content_type.lower():
        return False
    return True


class ReaderViewTest(BaseSiteTest):
    __doc__ = '\n    Is this page optimized for reader view?\n    See https://github.com/codelucas/newspaper/\n    '

    def on_page_parsed(self, page):
        from sitecomber.apps.results.models import PageTestResult
        if should_test_page(page):
            reader_view_enabled, status, message = is_reader_view_enabled(page, self.settings)
            r, created = PageTestResult.objects.get_or_create(page=page,
              test=(self.class_path))
            r.message = message
            r.status = status
            r.save()


class PlaceholderTextTest(BaseSiteTest):
    __doc__ = '\n    Looks for lorem or ipsum or tk in main article body and title\n    '

    def on_page_parsed(self, page):
        from sitecomber.apps.results.models import PageTestResult
        if should_test_page(page):
            placeholder_text, message = contains_placeholder_text(page, self.settings)
            status = PageTestResult.STATUS_SUCCESS if not placeholder_text else PageTestResult.STATUS_ERROR
            r, created = PageTestResult.objects.get_or_create(page=page,
              test=(self.class_path))
            r.message = message
            r.status = status
            r.save()


class ArticleReadTimeInfo(BaseSiteTest):
    __doc__ = '\n    Returns approximate read time based on 265WPM estimate\n    See https://pypi.org/project/readtime/\n    '

    def on_page_parsed(self, page):
        from sitecomber.apps.results.models import PageTestResult
        if should_test_page(page):
            message = get_article_readtime(page, self.settings)
            r, created = PageTestResult.objects.get_or_create(page=page,
              test=(self.class_path))
            r.message = message
            r.status = PageTestResult.STATUS_INFO
            r.save()


class SpellCheckTest(BaseSiteTest):
    __doc__ = '\n    Check spelling using pyspellchecker\n    See https://github.com/barrust/pyspellchecker\n    '

    def on_page_parsed(self, page):
        from sitecomber.apps.results.models import PageTestResult
        if should_test_page(page):
            contains_misspellings, message = check_spelling(page, self.settings)
            status = PageTestResult.STATUS_SUCCESS if not contains_misspellings else PageTestResult.STATUS_ERROR
            r, created = PageTestResult.objects.get_or_create(page=page,
              test=(self.class_path))
            r.message = message
            r.status = status
            r.save()