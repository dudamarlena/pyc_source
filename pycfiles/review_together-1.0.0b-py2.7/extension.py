# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/review_together/extension.py
# Compiled at: 2015-02-02 13:34:44
from reviewboard.extensions.base import Extension, JSExtension
from reviewboard.extensions.hooks import HeaderActionHook

class ReviewTogetherJSExtension(JSExtension):
    model_class = 'ReviewTogetherJS.Extension'


class ReviewTogether(Extension):
    default_settings = {'hub_url': ''}
    css_bundles = {'default': {'source_filenames': [
                                      'css/review-together.less']}}
    js_bundles = {'default': {'source_filenames': [
                                      'js/togetherjs.js',
                                      'js/review-together.js']}}
    is_configurable = True
    js_extensions = [
     ReviewTogetherJSExtension]

    def __init__(self, *args, **kwargs):
        super(ReviewTogether, self).__init__(*args, **kwargs)
        self.button = HeaderActionHook(self, [
         {'id': 'launch-together', 
            'label': 'Chat', 
            'url': '#'}])