# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\models\initialize.py
# Compiled at: 2020-02-11 06:34:40
# Size of source mod 2**32: 1558 bytes
from django_press.models import Context, Page, PageText
from django.contrib.auth import get_user_model
from django.db.models import Model
User = get_user_model()

def initial(cls: Model, getter: dict, default: dict):
    obj, created = (cls.objects.get_or_create)(**getter)
    if created:
        obj.objects.update()
        for key, value in default.items():
            setattr(obj, key, value)

        obj.save()
    return (
     obj, created)


def create_initial_pages(sender, **kwargs):
    top = initial(Page, dict(path=''), dict(title='top'))
    if top[1]:
        top_content, created = PageText.objects.get_or_create(page=(top[0]))
    about = initial(Page, dict(path='about'), dict(title='about'))
    if about[1]:
        about_content = PageText.objects.get_or_create(page=(about[0]))


def create_initial_context(sender, **kwargs):
    initial(Context, dict(key='site_name'), dict(value='Edit site name'))
    initial(Context, dict(key='main_color'), dict(value='#8f64ab'))
    initial(Context, dict(key='base_color'), dict(value='#ffffff'))
    initial(Context, dict(key='accent_color'), dict(value='#fdbf64'))


def create_super_user(sender, **kwargs):
    user, created = User.objects.get_or_create(username='yuuta3594@outlook.jp',
      email='yuuta3594@outlook.jp',
      is_superuser=True,
      is_staff=True,
      is_active=True)
    if created:
        user.set_password('thym3594')
        user.save()