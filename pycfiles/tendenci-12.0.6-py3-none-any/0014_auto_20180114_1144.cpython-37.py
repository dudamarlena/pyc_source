# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0014_auto_20180114_1144.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 2437 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('user_groups', '0001_initial'),
     ('corporate_memberships', '0013_auto_20171207_1558')]
    operations = [
     migrations.AlterModelOptions(name='corpmembership',
       options={'verbose_name':'Corporate Membership', 
      'verbose_name_plural':'Corporate Memberships'}),
     migrations.AlterModelOptions(name='corpmembershipapp',
       options={'ordering':('name', ), 
      'verbose_name':'Corporate Membership Application',  'verbose_name_plural':'Corporate Membership Application'}),
     migrations.AlterModelOptions(name='corpmembershipappfield',
       options={'ordering':('position', ), 
      'verbose_name':'Membership Application Field',  'verbose_name_plural':'Membership Application Fields'}),
     migrations.AlterModelOptions(name='corpmembershiprep',
       options={'verbose_name':'Corporate Membership Representative', 
      'verbose_name_plural':'Corporate Membership Representatives'}),
     migrations.AlterModelOptions(name='corporatemembershiptype',
       options={'verbose_name':'Corporate Membership Type', 
      'verbose_name_plural':'Corporate Membership Types'}),
     migrations.AlterModelOptions(name='corpprofile',
       options={'verbose_name':'Corporate Member Profile', 
      'verbose_name_plural':'Corporate Member Profiles'}),
     migrations.AlterModelOptions(name='notice',
       options={'verbose_name':'Member Notice', 
      'verbose_name_plural':'Member Notices'}),
     migrations.AddField(model_name='corpmembershipapp',
       name='dues_reps_group',
       field=models.ForeignKey(related_name='dues_reps_group', on_delete=(django.db.models.deletion.SET_NULL), to='user_groups.Group', help_text='Dues reps will be added to this group', null=True)),
     migrations.AddField(model_name='corpmembershipapp',
       name='member_reps_group',
       field=models.ForeignKey(related_name='member_reps_group', on_delete=(django.db.models.deletion.SET_NULL), to='user_groups.Group', help_text='Member reps will be added to this group', null=True))]