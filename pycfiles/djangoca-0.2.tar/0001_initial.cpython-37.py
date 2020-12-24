# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/oliver/06B092CEB092C419/Archivos/Proyectos/Python/Django/DjangoProjects/base_django/aplicaciones/usuarios/migrations/0001_initial.py
# Compiled at: 2019-05-29 21:47:22
# Size of source mod 2**32: 1254 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Usuario',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'password', models.CharField(max_length=128, verbose_name='password')),
      (
       'last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
      (
       'username', models.CharField(max_length=255, unique=True)),
      (
       'email', models.EmailField(max_length=255, unique=True, verbose_name='Correo Electrónico')),
      (
       'nombres', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombres')),
      (
       'apellidos', models.CharField(blank=True, max_length=255, null=True, verbose_name='Apellidos')),
      (
       'usuario_activo', models.BooleanField(default=True)),
      (
       'usuario_administrador', models.BooleanField(default=False))],
       options={'abstract': False})]