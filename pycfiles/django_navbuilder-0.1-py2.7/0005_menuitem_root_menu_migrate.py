# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/migrations/0005_menuitem_root_menu_migrate.py
# Compiled at: 2017-07-06 08:35:55
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

def do_save_work(context):
    """Adapted from the real save method because the real model is not
    available during a migration."""
    parent = context.parent
    while getattr(parent, b'parent', None) is not None:
        if parent is context:
            break
        parent = parent.parent

    if parent is not None:
        context.root_menu = parent.menu
    else:
        context.root_menu = context.menu
    context.save()
    for child in context.submenuitems.all():
        do_save_work(child)

    return


def set_root_menu(apps, schema_editor):
    MenuItem = apps.get_model(b'navbuilder', b'MenuItem')
    for obj in MenuItem.objects.filter(parent=None):
        obj.save()
        do_save_work(obj)

    return


class Migration(migrations.Migration):
    dependencies = [
     ('navbuilder', '0004_menuitem_root_menu')]
    operations = [
     migrations.RunPython(set_root_menu)]