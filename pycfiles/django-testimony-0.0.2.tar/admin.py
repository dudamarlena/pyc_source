# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/apps/django-testimony/testimony/admin.py
# Compiled at: 2014-01-10 19:02:43
from django.contrib import admin
from models import Testimonial, TestimonialProduct

class TestimonialProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(TestimonialProduct, TestimonialProductAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'published')
    list_editable = [
     'published']
    search_fields = [
     'author',
     'testimony']
    list_filter = [
     'published']
    list_per_page = 100
    list_select_related = True
    fieldsets = (
     (
      'General',
      {'description': 'General', 
         'fields': ('author', 'testimony', 'product')}),
     (
      'Admin',
      {'description': 'Publishing information bits.', 
         'fields': ('published', )}))


admin.site.register(Testimonial, TestimonialAdmin)