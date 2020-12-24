# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_extensions/files/views.py
# Compiled at: 2017-06-17 03:32:31
# Size of source mod 2**32: 2245 bytes
import json
from django.views.generic import View

class DocumentFileView(View):

    def form_valid(self, form, forms=None):
        body_json = json.loads(self.request.body.decode('utf-8'))
        if 'doc_path' in body_json and 'filename' in body_json['doc_path']:
            name_file = body_json['doc_path']['filename']
            self.request.name_file = name_file
            form.instance.name_file = name_file
        if forms:
            return super(DocumentFileView, self).form_valid(form, forms)
        else:
            return super(DocumentFileView, self).form_valid(form)


class ImageFileView(View):

    def form_valid(self, form, forms=None):
        body_json = json.loads(self.request.body.decode('utf-8'))
        if 'image' in body_json and 'filename' in body_json['image']:
            name_file = body_json['image']['filename']
            self.request.name_file = name_file
            form.instance.name_file = name_file
        else:
            field_image = '{}_image'.format(str(self.form_class).split('.')[(-1)].replace("'", '').replace('>', ''))
        if field_image in body_json and 'filename' in body_json[field_image]:
            name_file = body_json[field_image]['filename']
            self.request.name_file = name_file
            form.instance.name_file = name_file
        if forms:
            return super(ImageFileView, self).form_valid(form, forms)
        else:
            return super(ImageFileView, self).form_valid(form)