# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0006_transfer_language.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 806 bytes
from django.db import migrations

def transfer_lang(apps, schema_editor):
    Corpus = apps.get_model('explore', 'Corpus')
    Language = apps.get_model('explore', 'Language')
    for corpus in Corpus.objects.all():
        language, _ = Language.objects.get_or_create(name=(corpus.language))
        corpus.language_link = language
        corpus.save()
        language.save()


class Migration(migrations.Migration):
    dependencies = [
     ('explore', '0005_auto_20191210_1410')]
    operations = [
     migrations.RunPython(transfer_lang),
     migrations.RemoveField(model_name='corpus', name='language'),
     migrations.RenameField(model_name='corpus',
       old_name='language_link',
       new_name='language')]