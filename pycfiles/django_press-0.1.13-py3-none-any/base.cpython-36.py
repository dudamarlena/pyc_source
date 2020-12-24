# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\models\Inquiry\base.py
# Compiled at: 2019-12-19 11:27:31
# Size of source mod 2**32: 295 bytes
from polymorphic.models import PolymorphicModel

class BaseInquiry(PolymorphicModel):

    class Meta:
        verbose_name = '問い合わせ関連'
        verbose_name_plural = '問い合わせ関連'

    @classmethod
    def create_form(cls):
        raise NotImplementedError()