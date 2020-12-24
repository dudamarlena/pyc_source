# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/competition/view_modifiers.py
# Compiled at: 2010-08-04 03:48:25
from panya.view_modifiers import ViewModifier
from panya.view_modifiers.items import URLPatternItem
from django.core.urlresolvers import reverse

class CompetitionViewModifier(ViewModifier):

    def __init__(self, request, *args, **kwargs):
        self.items = [
         URLPatternItem(request, title='Current Competitions', path=reverse('competition_object_list', kwargs={}), matching_pattern_names=['competition_object_list'], default=False),
         URLPatternItem(request, title='Competition Rules', path=reverse('competition_preferences_detail', kwargs={}), matching_pattern_names=['competition_preferences_detail'], default=False)]
        super(CompetitionViewModifier, self).__init__(request, *args, **kwargs)