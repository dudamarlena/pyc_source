# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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