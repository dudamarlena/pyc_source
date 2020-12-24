# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Documents/LibraryApp/LibAppDjango/catalog/migrations/0002_auto_20190708_1432.py
# Compiled at: 2019-07-24 10:35:27
# Size of source mod 2**32: 2096 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('catalog', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Language',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)", max_length=200))]),
     migrations.AlterModelOptions(name='bookinstance',
       options={'ordering':[
       'due_back'], 
      'permissions':(('can_mark_returned', 'Set book as returned'), )}),
     migrations.AddField(model_name='bookinstance',
       name='borrower',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL))),
     migrations.AlterField(model_name='author',
       name='date_of_death',
       field=models.DateField(blank=True, null=True, verbose_name='died')),
     migrations.AlterField(model_name='bookinstance',
       name='status',
       field=models.CharField(blank=True, choices=[('d', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')], default='d', help_text='Book availability', max_length=1)),
     migrations.AlterField(model_name='genre',
       name='name',
       field=models.CharField(help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)', max_length=200)),
     migrations.AddField(model_name='book',
       name='language',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='catalog.Language'))]