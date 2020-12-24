# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dvs/Dropbox/Code/djangoql/test_project/core/migrations/0003_book_similar_books.py
# Compiled at: 2018-11-20 04:33:21
# Size of source mod 2**32: 397 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0002_book_genre')]
    operations = [
     migrations.AddField(model_name='book',
       name='similar_books',
       field=models.ManyToManyField(to='core.Book', blank=True))]