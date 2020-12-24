# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_i18n/djinn_i18n/views/po.py
# Compiled at: 2014-08-22 05:05:49
import json, polib
from django.views.generic import View
from django.http import HttpResponse
from djinn_i18n.tool import TOOL

class EntryEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, polib.POEntry):
            return {'msgid': obj.msgid, 'msgstr': obj.msgstr, 
               'comment': obj.comment, 
               'tcomment': obj.tcomment}
        return json.JSONEncoder.default(self, obj)


class POView(View):

    @property
    def locale(self):
        return self.kwargs.get('locale')

    def get(self, request, *args, **kwargs):
        entries = TOOL.get_entries(self.locale)
        return HttpResponse(json.dumps(entries, skipkeys=True, cls=EntryEncoder), content_type='application/json')