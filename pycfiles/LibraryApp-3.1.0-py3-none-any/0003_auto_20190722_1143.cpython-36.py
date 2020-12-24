# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Documents/LibraryApp/LibAppDjango/catalog/migrations/0003_auto_20190722_1143.py
# Compiled at: 2019-07-24 10:35:27
# Size of source mod 2**32: 1327 bytes
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
     ('catalog', '0002_auto_20190708_1432')]
    operations = [
     migrations.AlterField(model_name='book',
       name='isbn',
       field=models.CharField(help_text='13 Character <a href="isbn.org">ISBN number</a>', max_length=13, verbose_name='ISBN')),
     migrations.AlterField(model_name='book',
       name='summary',
       field=models.TextField(help_text='Enter a description of the book', max_length=1000)),
     migrations.AlterField(model_name='bookinstance',
       name='id',
       field=models.UUIDField(default=(uuid.uuid4), help_text='Unique ID for this book across library', primary_key=True, serialize=False)),
     migrations.AlterField(model_name='genre',
       name='name',
       field=models.CharField(help_text='Enter a book genre (e.g. Science Fiction etc.)', max_length=200)),
     migrations.AlterField(model_name='language',
       name='name',
       field=models.CharField(help_text="Enter the book's language)", max_length=200))]