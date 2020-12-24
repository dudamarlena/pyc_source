# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/i18n.py
# Compiled at: 2020-03-20 06:59:09
# Size of source mod 2**32: 2699 bytes
import os
from copy import copy
from flamingo.core.data_model import Q
INDEX_PAGE = '\n<!DOCTYPE html>\n<html>\n  <head>\n    <meta http-equiv="refresh" content="0; url=/{}/">\n  </head>\n  <body></body>\n</html>\n'

class I18N:

    def contents_parsed(self, context):
        content_key = getattr(context.settings, 'I18N_CONTENT_KEY', 'id')
        languages = getattr(context.settings, 'I18N_LANGUAGES', ['en', 'de'])
        default_language = getattr(context.settings, 'I18N_DEFAULT_LANGUAGE', 'en')
        enforce_redirect = getattr(context.settings, 'I18N_ENFORCE_REDIRECT', True)
        ignore = getattr(context.settings, 'I18N_IGNORE', {'i18n_ignore__isnull': False})
        for content in context.contents.exclude(ignore):
            if not content['lang']:
                content['lang'] = default_language
            if not content[content_key]:
                content[content_key] = content['path']
            translation_langs = (context.contents.filter)(**{content_key: content[content_key]}).values('lang')
            for l in languages:
                if l not in translation_langs:
                    content_data = copy(content.data)
                    content_data['original_path'] = content['path']
                    if 'path' in content_data:
                        content_data['i18n_path'] = content_data['path']
                        del content_data['path']
                    content_data['lang'] = l
                    (context.contents.add)(**content_data)

        for content in context.contents.exclude(ignore):
            content['output'] = os.path.join(content['lang'], content['output'])
            content['url'] = os.path.join('/', content['lang'], content['url'][1:])
            content['translations'] = context.contents.filter(Q(**{content_key: content[content_key]}), ~Q(lang=(content['lang'])))

        if enforce_redirect:
            (context.contents.add)(output='index.html', 
             url='/', 
             content_body=INDEX_PAGE.format(default_language), 
             redirect='/{}/'.format(default_language))