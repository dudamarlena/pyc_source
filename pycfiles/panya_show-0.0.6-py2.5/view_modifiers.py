# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/show/view_modifiers.py
# Compiled at: 2010-08-24 03:41:55
from panya.view_modifiers import ViewModifier
from panya.view_modifiers.items import URLPatternItem
from django.core.urlresolvers import reverse

class ShowContributorViewModifier(ViewModifier):

    def __init__(self, request, slug, *args, **kwargs):
        self.items = [
         URLPatternItem(request, title='Blog', path=reverse('showcontributor_content_list', kwargs={'slug': slug}), matching_pattern_names=['showcontributor_content_list', 'showcontributor_content_detail'], default=False),
         URLPatternItem(request, title='Profile', path=reverse('showcontributor_detail', kwargs={'slug': slug}), matching_pattern_names=['showcontributor_detail'], default=False),
         URLPatternItem(request, title='Contact', path=reverse('showcontributor_contact', kwargs={'slug': slug}), matching_pattern_names=['showcontributor_contact'], default=False),
         URLPatternItem(request, title='Appearances', path=reverse('showcontributor_appearance_list', kwargs={'slug': slug}), matching_pattern_names=['showcontributor_appearance_list'], default=False)]
        super(ShowContributorViewModifier, self).__init__(request)