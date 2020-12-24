# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/books/migrations/0005_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 3020 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('books', '0004_auto_20181026_1745')]
    operations = [
     migrations.AlterModelOptions(name='book',
       options={'verbose_name':'کتاب', 
      'verbose_name_plural':'کتاب ها'}),
     migrations.AlterModelOptions(name='booksegment',
       options={'verbose_name':'بخش کتاب', 
      'verbose_name_plural':'بخش کتاب ها'}),
     migrations.AlterModelOptions(name='publisher',
       options={'verbose_name':'منتشر کننده', 
      'verbose_name_plural':'منتشر کننده'}),
     migrations.AlterModelOptions(name='writertranslator',
       options={'verbose_name':'مترجم', 
      'verbose_name_plural':'مترجمین'}),
     migrations.AlterField(model_name='book',
       name='category_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='categories.Category', verbose_name='دسته بندی')),
     migrations.AlterField(model_name='book',
       name='published_date',
       field=models.DateTimeField(verbose_name='تاریخ انتشار')),
     migrations.AlterField(model_name='book',
       name='publisher_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='books.Publisher', verbose_name='منتشر کننده')),
     migrations.AlterField(model_name='book',
       name='sample_book',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='filefields.FileField', verbose_name='کتاب نمونه')),
     migrations.AlterField(model_name='book',
       name='translators_obj',
       field=models.ManyToManyField(blank=True, related_name='library_translators', to='books.WriterTranslator', verbose_name='مترجمین')),
     migrations.AlterField(model_name='book',
       name='writers_obj',
       field=models.ManyToManyField(related_name='library_writers', to='books.WriterTranslator', verbose_name='نویسنده ها')),
     migrations.AlterField(model_name='publisher',
       name='title',
       field=models.CharField(max_length=255, verbose_name='عنوان')),
     migrations.AlterField(model_name='writertranslator',
       name='first_name',
       field=models.CharField(max_length=60, verbose_name='نام')),
     migrations.AlterField(model_name='writertranslator',
       name='last_name',
       field=models.CharField(max_length=60, verbose_name='نام خانوادگی'))]