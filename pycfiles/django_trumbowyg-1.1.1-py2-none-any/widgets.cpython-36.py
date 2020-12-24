# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/est/src/django-trumbowyg/trumbowyg/widgets.py
# Compiled at: 2019-03-21 10:48:51
# Size of source mod 2**32: 2741 bytes
from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from . import settings
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

def get_trumbowyg_language():
    """
    Convert language from django to trumbowyg format

    Example:
        Django uses: pt-br and trumbowyg use pt_br
    """
    return get_language().replace('-', '_')


class TrumbowygWidget(Textarea):

    class Media:
        css = {'all': ('trumbowyg/ui/trumbowyg.css', 'trumbowyg/admin.css')}
        js = [
         '//ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js',
         'trumbowyg/trumbowyg.min.js',
         'trumbowyg/plugins/upload/trumbowyg.upload.js',
         'trumbowyg/langs/{0}.min.js'.format(get_trumbowyg_language())]

    def render(self, name, value, attrs=None, renderer=None):
        output = super(TrumbowygWidget, self).render(name, value, attrs)
        script = '\n            <script>\n                $("#id_{name}").trumbowyg({{\n                    lang: "{lang}",\n                    semantic: {semantic},\n                    resetCss: true,\n                    autogrow: true,\n                    removeformatPasted: true,\n                    btnsDef: {{\n                        image: {{\n                            dropdown: ["upload", "insertImage", "base64", "noembed"],\n                            ico: "insertImage"\n                        }}\n                    }},\n                    btns: [\n                        ["formatting"],\n                        "btnGrp-semantic",\n                        ["link"],\n                        ["image"],\n                        "btnGrp-justify",\n                        "btnGrp-lists",\n                        ["horizontalRule"],\n                        ["removeformat"],\n                        ["viewHTML"],\n                        ["fullscreen"]\n                    ],\n                    plugins: {{\n                        upload: {{\n                            serverPath: "{path}",\n                            fileFieldName: "image",\n                            statusPropertyName: "message",\n                            urlPropertyName: "file"\n                        }}\n                    }}\n                }});\n            </script>\n        '.format(name=name,
          lang=(get_trumbowyg_language()),
          semantic=(settings.SEMANTIC),
          path=(reverse('trumbowyg_upload_image')))
        output += mark_safe(script)
        return output