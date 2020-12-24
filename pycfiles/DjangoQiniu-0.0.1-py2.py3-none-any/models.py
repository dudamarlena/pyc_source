# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangyong/my_development/python/django_pro/bookstore/DjangoQiniu/models.py
# Compiled at: 2017-05-10 03:48:34
from django.db import models
from .widgets import QiniuWidget

class QiniuField(models.CharField):

    def __init__(self, qiniu_field, btn_title='上传文件', *args, **kwargs):
        self.qiniu_field = qiniu_field
        self.btn_title = btn_title
        super(QiniuField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(QiniuField, self).deconstruct()
        kwargs['qiniu_field'] = self.qiniu_field
        kwargs['btn_title'] = self.btn_title
        return (name, path, args, kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = QiniuWidget(btn_title=self.btn_title, qiniu_field=self.qiniu_field)
        return super(QiniuField, self).formfield(**kwargs)