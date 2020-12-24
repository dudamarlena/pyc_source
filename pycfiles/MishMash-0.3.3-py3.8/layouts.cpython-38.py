# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/web/layouts.py
# Compiled at: 2019-12-04 00:39:07
# Size of source mod 2**32: 557 bytes
import gettext
from pyramid_layout.layout import layout_config
_ = gettext.gettext

@layout_config(name='main-layout',
  template='mishmash.web:templates/layouts/main-layout.pt')
class AppLayout:

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.home_url = request.application_url
        self.headings = []

    @property
    def page_title(self):
        return _('MishMash music!')

    def add_heading(self, name, *args, **kw):
        self.headings.append((name, args, kw))