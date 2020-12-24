# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: share/urlwatch/examples/hooks.py.example
# Compiled at: 2019-01-27 05:47:14
# Size of source mod 2**32: 4014 bytes
import re
from urlwatch import filters
from urlwatch import jobs
from urlwatch import reporters

class CustomMatchUrlFilter(filters.AutoMatchFilter):
    MATCH = {'url': 'http://example.org/'}

    def filter(self, data):
        return data.replace('foo', 'bar')


class CustomRegexMatchUrlFilter(filters.RegexMatchFilter):
    MATCH = {'url': re.compile('http://example.org/.*')}

    def filter(self, data):
        return data.replace('foo', 'bar')


class CustomTextFileReporter(reporters.TextReporter):
    __doc__ = 'Custom reporter that writes the text-only report to a file'
    __kind__ = 'custom_file'

    def submit(self):
        with open(self.config['filename'], 'w') as (fp):
            fp.write('\n'.join(super().submit()))


class CustomHtmlFileReporter(reporters.HtmlReporter):
    __doc__ = 'Custom reporter that writes the HTML report to a file'
    __kind__ = 'custom_html'

    def submit(self):
        with open(self.config['filename'], 'w') as (fp):
            fp.write('\n'.join(super().submit()))