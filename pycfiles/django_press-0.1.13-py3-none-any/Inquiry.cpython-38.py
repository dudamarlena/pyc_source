# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\admin\Inquiry.py
# Compiled at: 2019-12-19 18:31:38
# Size of source mod 2**32: 673 bytes
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from django_press.models import BaseInquiry, Contact

class InquiryChildAdmin(PolymorphicChildModelAdmin):
    base_model = BaseInquiry


class ContactAdmin(InquiryChildAdmin):
    base_model = Contact
    list_display = ('category', 'name', 'email', 'body', 'created_at')


class InquiryAdmin(PolymorphicParentModelAdmin):
    base_model = BaseInquiry
    child_models = (Contact,)
    list_filter = (PolymorphicChildModelFilter,)