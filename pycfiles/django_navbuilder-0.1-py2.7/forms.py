# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/forms.py
# Compiled at: 2017-07-06 08:35:55
from django import forms
from navbuilder.models import Menu, MenuItem

class MenuAdminForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ['title', 'slug']


class MenuItemAdminForm(forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = [
         'title', 'slug', 'position', 'menu', 'parent', 'target',
         'link_content_type', 'link_object_id']