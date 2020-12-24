# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/pages/migrations/0005_auto_20191103_1240.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 3575 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Page = apps.get_model('pages', 'Page')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    key = ''
    try:
        key = 'home'
        Page.objects.get(english_title=key)
    except Exception:
        Page.objects.create(title='صفحه اصلی',
          english_title=key,
          is_show_in_home=True)

    try:
        key = 'library'
        Page.objects.get(english_title=key)
    except Exception:
        Page.objects.create(title='کتابخانه',
          english_title=key,
          is_show_in_home=False)

    try:
        key = 'category'
        Page.objects.get(english_title=key)
    except Exception:
        Page.objects.create(title='دسته بندی',
          english_title=key,
          is_show_in_home=False)

    try:
        key = 'contact_us'
        Page.objects.get(english_title=key)
    except Exception:
        Page.objects.create(title='تماس با ما',
          english_title=key,
          is_show_in_home=False)

    try:
        key = 'about_us'
        Page.objects.get(english_title=key)
    except Exception:
        Page.objects.create(title='درباره ما',
          english_title=key,
          is_show_in_home=False)

    try:
        key = 'my_products'
        Page.objects.get(english_title=key)
    except Exception:
        Page.objects.create(title='محصولات من',
          english_title=key,
          is_show_in_home=False)

    try:
        key = 'download_manager'
        Page.objects.get(english_title=key)
    except Exception:
        Page.objects.create(title='دانلود منیجر',
          english_title=key,
          is_show_in_home=False)

    try:
        key = 'file_manager'
        Page.objects.get(english_title=key)
    except Exception:
        Page.objects.create(title='مدیریت فایل',
          english_title=key,
          is_show_in_home=False)

    try:
        key = 'user_invitation'
        Page.objects.get(english_title=key)
    except Exception:
        Page.objects.create(title='دعوت از دوستان',
          english_title=key,
          is_show_in_home=False)

    new_ct = ContentType.objects.get_for_model(Page)
    Page.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Page = apps.get_model('pages', 'Page')
    keys = [
     'home',
     'library',
     'category',
     'contact_us',
     'about_us',
     'my_products',
     'download_manager',
     'file_manager',
     'user_invitation']
    for key in keys:
        try:
            Page.objects.get(english_title=key).delete()
        except Exception:
            pass


class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0004_auto_20190114_1537')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]