# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0023_auto_20180919_1526.py
# Compiled at: 2019-04-03 22:56:26
# Size of source mod 2**32: 3458 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from django.core.validators import MinValueValidator

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0022_auto_20180823_1947')]
    operations = [
     migrations.AddField(model_name='eventlistpluginmodel',
       name='eventCategories',
       field=models.ManyToManyField(blank=True, help_text='Leave blank for no restriction', to='core.PublicEventCategory', verbose_name='Limit to public event categories')),
     migrations.AddField(model_name='eventlistpluginmodel',
       name='levels',
       field=models.ManyToManyField(blank=True, help_text='Leave blank for no restriction', to='core.DanceTypeLevel', verbose_name='Limit to type and levels')),
     migrations.AddField(model_name='eventlistpluginmodel',
       name='limitNumber',
       field=models.PositiveSmallIntegerField(blank=True, help_text='Leave blank for no restriction', null=True, verbose_name='Limit number')),
     migrations.AddField(model_name='eventlistpluginmodel',
       name='seriesCategories',
       field=models.ManyToManyField(blank=True, help_text='Leave blank for no restriction', to='core.SeriesCategory', verbose_name='Limit to series categories')),
     migrations.AddField(model_name='eventlistpluginmodel',
       name='sortOrder',
       field=models.CharField(choices=[('A', 'Ascending'), ('D', 'Descending')], default='A', help_text='This may be overridden by the particular template in use', max_length=1, verbose_name='Sort by start time')),
     migrations.RemoveField(model_name='eventlistpluginmodel',
       name='location'),
     migrations.AddField(model_name='eventlistpluginmodel',
       name='location',
       field=models.ManyToManyField(blank=True, help_text='Leave blank for no restriction', to='core.Location', verbose_name='Limit to locations')),
     migrations.CreateModel(name='EventDJ',
       fields=[],
       options={'verbose_name':'Event DJ', 
      'verbose_name_plural':'Event DJs', 
      'proxy':True, 
      'indexes':[]},
       bases=('core.eventstaffmember', )),
     migrations.AddField(model_name='eventstaffmember',
       name='specifiedHours',
       field=models.FloatField(blank=True, help_text='If unspecified, then the net number of hours is based on the duration of the applicable event occurrences.', null=True, validators=[MinValueValidator(0)], verbose_name='Number of hours (optional)')),
     migrations.AddField(model_name='classdescription',
       name='shortDescription',
       field=models.TextField(blank=True, help_text='May be used for tag lines and feeds.', verbose_name='Short description')),
     migrations.AddField(model_name='publicevent',
       name='shortDescriptionField',
       field=models.TextField(blank=True, help_text='Shorter description for "taglines" and feeds.', null=True, verbose_name='Short description'))]