# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/migrations/0004_load_skills_and_causes.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1337 bytes
from __future__ import unicode_literals
from django.db import migrations
skills = [
 'Arts/Handcrafting', 'Communication', 'Dance/Music', 'Law', 'Education', 'Sports', 'Cooking', 'Management', 'Idioms', 'Computers/Technology', 'Health', 'Others']
causes = ['Professional Training', 'Fight Poverty', 'Conscious consumption', 'Culture, Sport and Art', 'Human Rights', 'Education', 'Youth', 'Elders', 'Environment', 'Citizen Participation', 'Animal Protection', 'Health', 'People with disabilities']

def load_data(apps, schema_editor):
    Skill = apps.get_model('ovp_core', 'Skill')
    Cause = apps.get_model('ovp_core', 'Cause')
    for skill in skills:
        s = Skill(name=skill)
        s.save()

    for cause in causes:
        c = Cause(name=cause)
        c.save()


def unload_data(apps, schema_editor):
    Skill = apps.get_model('ovp_core', 'Skill')
    Cause = apps.get_model('ovp_core', 'Cause')
    for skill in skills:
        s = Skill.objects.filter(name=skill)
        s.delete()

    for cause in causes:
        c = Cause.objects.filter(name=cause)
        c.delete()


class Migration(migrations.Migration):
    dependencies = [
     ('ovp_core', '0003_cause_skill')]
    operations = [
     migrations.RunPython(load_data, reverse_code=unload_data)]