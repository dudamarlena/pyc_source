# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/tasks/tasks.py
# Compiled at: 2018-02-23 10:12:38
# Size of source mod 2**32: 2754 bytes
import uuid, django_rq
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
from rq.decorators import job
from ..manager import Manager
from ..export import ImportBo, ExportBo

def do_action(action, model_class, item_id, languages=None, update_item_languages=False):
    manager = Manager()
    manager.bulk_mode = True
    main_lang_code = manager.get_main_language()
    if languages and main_lang_code in languages:
        languages.remove(main_lang_code)
    try:
        item = model_class.objects.language(main_lang_code).get(pk=item_id)
    except model_class.DoesNotExist:
        return

    if action == 'create':
        manager.create_translations_for_item_and_its_children(item, languages)
        if update_item_languages:
            manager.add_item_languages(item, languages)
    elif action == 'delete':
        manager.delete_translations_for_item_and_its_children(item, languages)
    if update_item_languages:
        manager.remove_item_languages(item, languages)


@job('default', connection=django_rq.get_connection('default'))
def create_translations_for_item_and_its_children(model_class, item_id, languages=None, update_item_languages=False):
    do_action('create', model_class, item_id, languages, update_item_languages)


@job('default', connection=django_rq.get_connection('default'))
def delete_translations_for_item_and_its_children(model_class, item_id, languages=None, update_item_languages=False):
    do_action('delete', model_class, item_id, languages, update_item_languages)


@job('default', connection=django_rq.get_connection('default'))
def import_translations_from_excel(file, user_id):
    from ..views import ImportExportNotificationView
    user = User.objects.get(pk=user_id)
    errors = ImportBo().import_translations(file)
    ImportExportNotificationView(user=user, errors=errors).send(to=(user.email,))


@job('default', connection=django_rq.get_connection('default'))
def export_translations_to_excel(task_ids, user_id):
    from ..views import ImportExportNotificationView
    from ..models import TransUserExport
    user = User.objects.get(pk=user_id)
    bin_file = ExportBo().export_translations(task_ids)
    if bin_file:
        filename = 'export-user-{}.xls'.format(user_id)
        user_export = TransUserExport.objects.create(user=user, uuid=uuid.uuid4())
        user_export.file.save(filename, ContentFile(bin_file))
        errors = None
    else:
        user_export = None
        errors = [_('No se ha podido generar el archivo')]
    ImportExportNotificationView(user=user, user_export=user_export, errors=errors).send(to=(user.email,))