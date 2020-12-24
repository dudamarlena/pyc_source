# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\pc\Workspace\Django\zivjulete\admin_multilanguage\views.py
# Compiled at: 2018-12-04 21:16:32
# Size of source mod 2**32: 650 bytes
from django.views.generic import View
from django.shortcuts import redirect
from django.conf import settings

class ChangeLanguageView(View):

    def get(self, request):
        language = request.GET.get('language', None)
        current_path = request.GET.get('current_path', None)
        for setting_language in settings.LANGUAGES:
            if language == setting_language[0]:
                if current_path:
                    request.session['_language'] = language
                    return redirect(current_path)
                raise ValidationError('"current_path" is impoperly configured')