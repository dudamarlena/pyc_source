# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbmozui/extension.py
# Compiled at: 2015-02-13 17:19:00
from __future__ import unicode_literals
from rbmozui.fields import CommitsListField
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import ReviewRequestFieldsHook, TemplateHook
from reviewboard.reviews.builtin_fields import TargetPeopleField, TestingDoneField
from reviewboard.reviews.fields import get_review_request_field, get_review_request_fieldset
from reviewboard.urls import diffviewer_url_names, review_request_url_names

class RBMozUI(Extension):
    metadata = {b'Name': b'rbmozui', 
       b'Summary': b'UI tweaks to Review Board for Mozilla'}
    css_bundles = {b'commits': {b'source_filenames': [
                                        b'css/commits.less']}, 
       b'default': {b'source_filenames': [
                                        b'css/common.css']}, 
       b'review': {b'source_filenames': [
                                       b'css/review.less']}, 
       b'viewdiff': {b'source_filenames': [
                                         b'css/viewdiff.less']}}
    js_bundles = {b'commits': {b'source_filenames': [
                                        b'js/commits.js']}, 
       b'rbmozuiautocomplete': {b'source_filenames': [
                                                    b'js/ui.rbmozuiautocomplete.js']}, 
       b'review': {b'source_filenames': [
                                       b'js/review.js']}}

    def initialize(self):
        main_fieldset = get_review_request_fieldset(b'main')
        testing_done_field = get_review_request_field(b'testing_done')
        if testing_done_field:
            main_fieldset.remove_field(testing_done_field)
        TemplateHook(self, b'base-css', b'rbmozui/commits-stylings-css.html', apply_to=b'rbmozui-commits')
        TemplateHook(self, b'base-css', b'rbmozui/review-stylings-css.html', apply_to=review_request_url_names + [b'rbmozui-commits'])
        TemplateHook(self, b'base-css', b'rbmozui/viewdiff-stylings-css.html', apply_to=diffviewer_url_names)
        TemplateHook(self, b'base-scripts-post', b'rbmozui/review-scripts-js.html', apply_to=review_request_url_names)
        TemplateHook(self, b'base-scripts-post', b'rbmozui/commits-scripts-js.html', apply_to=review_request_url_names)
        ReviewRequestFieldsHook(self, b'main', [CommitsListField])
        main_fieldset.field_classes.insert(0, main_fieldset.field_classes.pop())

    def shutdown(self):
        main_fieldset = get_review_request_fieldset(b'main')
        testing_done_field = get_review_request_field(b'testing_done')
        if not testing_done_field:
            main_fieldset.add_field(TestingDoneField)
        super(RBMozUI, self).shutdown()