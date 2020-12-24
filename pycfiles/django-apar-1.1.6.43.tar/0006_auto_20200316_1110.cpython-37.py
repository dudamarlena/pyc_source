# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/books/migrations/0006_auto_20200316_1110.py
# Compiled at: 2020-03-16 03:40:40
# Size of source mod 2**32: 2919 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('books', '0005_auto_20190615_1430')]
    operations = [
     migrations.AlterModelOptions(name='book',
       options={'verbose_name':'Book', 
      'verbose_name_plural':'Books'}),
     migrations.AlterModelOptions(name='booksegment',
       options={'verbose_name':'Book Segment', 
      'verbose_name_plural':'Book Segments'}),
     migrations.AlterModelOptions(name='publisher',
       options={'verbose_name':'Publisher', 
      'verbose_name_plural':'Publishers'}),
     migrations.AlterModelOptions(name='writertranslator',
       options={'verbose_name':'Writer Translator', 
      'verbose_name_plural':'Writers Translators'}),
     migrations.AlterField(model_name='book',
       name='category_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='categories.Category', verbose_name='Category')),
     migrations.AlterField(model_name='book',
       name='published_date',
       field=models.DateTimeField(verbose_name='Published Date')),
     migrations.AlterField(model_name='book',
       name='publisher_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='books.Publisher', verbose_name='Publisher')),
     migrations.AlterField(model_name='book',
       name='sample_book',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='filefields.FileField', verbose_name='Sample Book')),
     migrations.AlterField(model_name='book',
       name='translators_obj',
       field=models.ManyToManyField(blank=True, related_name='library_translators', to='books.WriterTranslator', verbose_name='Translators')),
     migrations.AlterField(model_name='book',
       name='writers_obj',
       field=models.ManyToManyField(related_name='library_writers', to='books.WriterTranslator', verbose_name='Writers')),
     migrations.AlterField(model_name='publisher',
       name='title',
       field=models.CharField(max_length=255, verbose_name='Title')),
     migrations.AlterField(model_name='writertranslator',
       name='first_name',
       field=models.CharField(max_length=60, verbose_name='First Name')),
     migrations.AlterField(model_name='writertranslator',
       name='last_name',
       field=models.CharField(max_length=60, verbose_name='Last Name'))]