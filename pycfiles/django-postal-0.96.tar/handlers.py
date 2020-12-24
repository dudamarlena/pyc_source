# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mick/src/django-postal/src/postal/api/handlers.py
# Compiled at: 2015-03-03 03:42:01
from ..handler import BaseHandler
from postal.library import form_factory

class PostalHandler(BaseHandler):
    allowed_methods = ('GET', )

    def read(self, request):
        iso_code = request.GET.get('country', '')
        json = {}
        form_class = form_factory(country_code=iso_code)
        form_obj = form_class()
        for k, v in form_obj.fields.items():
            if k not in json.keys():
                json[k] = {}
            json[k]['label'] = unicode(v.label)
            json[k]['widget'] = v.widget.render(k, '', attrs={'id': 'id_' + k})

        return json