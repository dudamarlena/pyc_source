# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reddit2ebook/ebooklib_patched/plugins/base.py
# Compiled at: 2016-05-13 06:16:04
# Size of source mod 2**32: 1546 bytes


class BasePlugin(object):

    def before_write(self, book):
        """Processing before save"""
        return True

    def after_write(self, book):
        """Processing after save"""
        return True

    def before_read(self, book):
        """Processing before save"""
        return True

    def after_read(self, book):
        """Processing after save"""
        return True

    def item_after_read(self, book, item):
        """Process general item after read."""
        return True

    def item_before_write(self, book, item):
        """Process general item before write."""
        return True

    def html_after_read(self, book, chapter):
        """Processing HTML before read."""
        return True

    def html_before_write(self, book, chapter):
        """Processing HTML before save."""
        return True