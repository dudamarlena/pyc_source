# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/est/src/django-trumbowyg/trumbowyg/widgets.py
# Compiled at: 2017-09-09 21:05:22
# Size of source mod 2**32: 2354 bytes
from django.conf import settings
from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, get_language_info
from django.core.urlresolvers import reverse

class TrumbowygWidget(Textarea):

    class Media:
        css = {'all': ('trumbowyg/ui/trumbowyg.css', 'trumbowyg/admin.css')}
        js = [
         '//ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js',
         'trumbowyg/trumbowyg.min.js',
         'trumbowyg/plugins/upload/trumbowyg.upload.js'] + ['trumbowyg/langs/%s.min.js' % x[0] for x in settings.LANGUAGES]

    def render(self, name, value, attrs=None):
        output = super(TrumbowygWidget, self).render(name, value, attrs)
        script = '\n            <script>\n                $("#id_%s").trumbowyg({\n                    lang: "%s",\n                    semantic: true,\n                    resetCss: true,\n                    autogrow: true,\n                    removeformatPasted: true,\n                    btnsDef: {\n                        image: {\n                            dropdown: [\'upload\', \'insertImage\', \'base64\', \'noembed\'],\n                            ico: \'insertImage\'\n                        }\n                    },\n                    btns: [\n                        [\'formatting\'],\n                        \'btnGrp-semantic\',\n                        [\'link\'],\n                        [\'image\'],\n                        \'btnGrp-justify\',\n                        \'btnGrp-lists\',\n                        \'video\',\n                        [\'horizontalRule\'],\n                        [\'removeformat\'],\n                        [\'fullscreen\'],\n                        [\'viewHTML\']\n                    ],\n                    plugins: {\n                        upload: {\n                            serverPath: \'%s\',\n                            fileFieldName: \'image\',\n                            statusPropertyName: \'message\',\n                            urlPropertyName: \'file\'\n                        }\n                    }\n                });\n            </script>\n        ' % (name, get_language_info(get_language())['code'], reverse('trumbowyg_upload_image'))
        output += mark_safe(script)
        return output