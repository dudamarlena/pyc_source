# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dvs/Dropbox/Code/djangoql/test_project/core/migrations/0004_book_similar_books_related_name.py
# Compiled at: 2018-11-20 15:58:13
# Size of source mod 2**32: 901 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0003_book_similar_books')]
    operations = [
     migrations.AlterField(model_name='book',
       name='content_type',
       field=models.ForeignKey(editable=False, null=True, on_delete=(django.db.models.deletion.CASCADE), to='contenttypes.ContentType')),
     migrations.AlterField(model_name='book',
       name='object_id',
       field=models.PositiveIntegerField(editable=False, null=True)),
     migrations.AlterField(model_name='book',
       name='similar_books',
       field=models.ManyToManyField(blank=True, related_name='_book_similar_books_+', to='core.Book'))]