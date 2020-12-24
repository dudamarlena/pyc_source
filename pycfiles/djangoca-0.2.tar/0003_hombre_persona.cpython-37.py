# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oliver/Documentos/Proyectos/base_django/aplicaciones/base/migrations/0003_hombre_persona.py
# Compiled at: 2019-07-28 03:45:00
# Size of source mod 2**32: 1445 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('base', '0002_delete_modeloprueba')]
    operations = [
     migrations.CreateModel(name='Persona',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'nombres', models.CharField(max_length=200, verbose_name='Nombre de Persona')),
      (
       'apellidos', models.CharField(max_length=200, verbose_name='Nombre de Persona')),
      (
       'content_type', models.ForeignKey(editable=False, null=True, on_delete=(django.db.models.deletion.CASCADE), to='contenttypes.ContentType'))],
       options={'abstract': False}),
     migrations.CreateModel(name='Hombre',
       fields=[
      (
       'persona_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='base.Persona')),
      (
       'mayor', models.BooleanField())],
       options={'abstract': False},
       bases=('base.persona', ))]