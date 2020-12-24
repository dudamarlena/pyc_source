# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangyong/my_development/python/django_pro/bookstore/DjangoQiniu/widgets.py
# Compiled at: 2017-05-10 03:48:57
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.conf import settings

class QiniuWidget(forms.TextInput):

    def __init__(self, *args, **kwargs):
        self.btn_title = kwargs.pop('btn_title')
        self.qiniu_field = kwargs.pop('qiniu_field')
        super(QiniuWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        context = {'qiniu_domain': settings.QINIU_DOMAIN, 
           'qiniu_field_name': self.qiniu_field, 
           'qiniu_field_value': value, 
           'btn_title': self.btn_title}
        return mark_safe(render_to_string('qiniu.html', context=context))

    def value_from_datadict(self, data, files, name):
        return data.get(name)