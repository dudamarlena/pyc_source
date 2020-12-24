# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/rbstopwatch/extension.py
# Compiled at: 2015-11-30 19:18:58
from __future__ import unicode_literals
from reviewboard.extensions.base import Extension, JSExtension
from reviewboard.extensions.hooks import TemplateHook
from reviewboard.urls import reviewable_url_names, review_request_url_names
_apply_to_url_names = set(reviewable_url_names + review_request_url_names)

class StopwatchJSExtension(JSExtension):
    """Javascript extension for the stopwatch."""
    model_class = b'RBStopwatch.Extension'
    apply_to = _apply_to_url_names


class StopwatchExtension(Extension):
    """A stopwatch extension.

    This extension adds a bit of UI to every review request page that gives
    reviewers a "stopwatch" which allows them to turn on and off a timer. The
    total time spent reviewing will be added to the Review's extra_data.
    """
    metadata = {b'Name': b'Review Stopwatch', 
       b'Summary': b'A stopwatch for reviewers: keep track of the total time spent on each code review.'}
    js_extensions = [
     StopwatchJSExtension]
    css_bundles = {b'default': {b'source_filenames': [
                                        b'css/stopwatch.less'], 
                    b'apply_to': _apply_to_url_names}}
    js_bundles = {b'default': {b'source_filenames': [
                                        b'js/stopwatch.js'], 
                    b'apply_to': _apply_to_url_names}}

    def initialize(self):
        """Initialize the extension."""
        TemplateHook(self, b'review-summary-header-post', b'rbstopwatch-review-header.html', apply_to=[
         b'review-request-detail'])