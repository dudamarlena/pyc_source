# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rowan/Nyaruka/dash/dash_test_runner/testapp/views.py
# Compiled at: 2018-08-14 12:18:01
# Size of source mod 2**32: 307 bytes
from smartmin.views import SmartCRUDL, SmartTemplateView
from dash_test_runner.testapp.models import Contact

class ContactCRUDL(SmartCRUDL):
    model = Contact
    actions = ('test_tags', 'list')

    class TestTags(SmartTemplateView):
        permission = None
        template_name = 'tags_test.html'