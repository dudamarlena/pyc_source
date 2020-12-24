# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/views.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 3814 bytes
from collections import defaultdict
from django.contrib.admin.views.main import ChangeList
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.http.response import HttpResponseForbidden
from django.views import View
from translation_manager.models import TranslationEntry
from .settings import get_settings
hint_sql_template = "SELECT te2.* FROM %s AS te1 INNER JOIN %s AS te2 ON (te1.original = te2.original AND te1.domain = te2.domain AND te2.locale_path = %s) WHERE te2.is_published='1' AND te1.id IN (%s) AND te2.language = '%s'"

class TranslationChangeList(ChangeList):

    def __init__(self, *args, **kwargs):
        (super(TranslationChangeList, self).__init__)(*args, **kwargs)
        if self.result_list:
            self.prep_hints()

    def prep_hints(self):
        entry_ids = [str(entry.id) for entry in self.result_list]
        hint_locale = get_settings('TRANSLATIONS_HINT_LANGUAGE_FORCED_RELATIVE_LOCALE_PATH')
        if not hint_locale:
            hint_locale = 'te1.locale_path'
        else:
            hint_locale = "'%s'" % hint_locale
        hint_sql = hint_sql_template % (
         TranslationEntry._meta.db_table,
         TranslationEntry._meta.db_table,
         hint_locale,
         ','.join(entry_ids),
         get_settings('TRANSLATIONS_HINT_LANGUAGE'))
        hint_qs = TranslationEntry.objects.raw(hint_sql)
        hint_dict = dict([(hint.original, hint.translation) for hint in hint_qs])
        for result in self.result_list:
            result._hint = hint_dict.get(result.original, '')


if get_settings('TRANSLATIONS_ENABLE_API_COMMUNICATION'):
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework.permissions import AllowAny
    from translation_manager.serializers import TranslationSerializer
    from translation_manager.utils import filter_queryset

    class TranslationListView(APIView):
        __doc__ = '\n        get translations in selected language in json\n        '
        authentication_classes = get_settings('TRANSLATIONS_API_AUTHENTICATION_CLASSES') if get_settings('TRANSLATIONS_API_AUTHENTICATION_CLASSES') else ()
        permission_classes = get_settings('TRANSLATIONS_API_PERMISSION_CLASSES') if get_settings('TRANSLATIONS_API_PERMISSION_CLASSES') else (AllowAny,)

        def get(self, request, language, format=None):
            """
            Return a list of all translations for selected language.
            """
            queryset = filter_queryset(TranslationEntry.objects.filter(language=language), get_settings('TRANSLATIONS_API_QUERYSET_FORCE_FILTERS'))
            if not get_settings('TRANSLATIONS_API_RETURN_ALL'):
                queryset = queryset.exclude(Q(translation__isnull=True) | Q(translation__exact=''))
            result = {}
            for object in queryset:
                result[object.original] = object.translation

            return Response(result)


class SyncView(View):

    def get(self, request):
        token = request.GET.get('token')
        if not token or token != settings.TRANSLATIONS_SYNC_LOCAL_TOKEN:
            return HttpResponseForbidden()
        else:
            translations = TranslationEntry.objects.all()
            data = defaultdict(dict)
            for entry in translations:
                data[entry.language].setdefault(entry.domain, defaultdict(dict))[entry.original] = dict(translation=(entry.translation), changed=(entry.changed))

            return JsonResponse(data)