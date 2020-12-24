# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\models\initialize.py
# Compiled at: 2020-02-09 09:15:26
# Size of source mod 2**32: 1537 bytes
from django_press.models import Context, Page, PageText
from django.contrib.auth import get_user_model
User = get_user_model()

def create_initial_pages(sender, **kwargs):
    top = Page.objects.get_or_create(title='top', path='')
    top_content = PageText.objects.get_or_create(page=(top[0]))
    about = Page.objects.get_or_create(title='about', path='about')
    about_content = PageText.objects.get_or_create(page=(about[0]))


def create_initial_context(sender, **kwargs):
    site_name, created = Context.objects.get_or_create(key='site_name')
    if created:
        site_name.value = 'Edit site name'
        site_name.save()
    main_color, created = Context.objects.get_or_create(key='main_color')
    if created:
        main_color.value = '#8f64ab'
        main_color.save()
    base_color, created = Context.objects.get_or_create(key='base_color')
    if created:
        base_color.value = '#ffffff'
        base_color.save()
    accent_color, created = Context.objects.get_or_create(key='accent_color')
    if created:
        accent_color.value = '#fdbf64'
        accent_color.save()


def create_super_user(sender, **kwargs):
    user, created = User.objects.get_or_create(username='yuuta3594@outlook.jp',
      email='yuuta3594@outlook.jp',
      is_superuser=True,
      is_staff=True,
      is_active=True)
    if created:
        user.set_password('thym3594')
        user.save()