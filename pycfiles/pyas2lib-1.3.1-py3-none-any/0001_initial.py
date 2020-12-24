# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./pyas2/migrations/0001_initial.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import models, migrations
import django.core.files.storage

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Log', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'timestamp', models.DateTimeField(auto_now_add=True)),
      (
       b'status', models.CharField(max_length=2, choices=[('S', 'Success'), ('E', 'Error'), ('W', 'Warning')])),
      (
       b'text', models.CharField(max_length=255))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'MDN', fields=[
      (
       b'message_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
      (
       b'timestamp', models.DateTimeField(auto_now_add=True)),
      (
       b'status', models.CharField(max_length=2, choices=[('S', 'Sent'), ('R', 'Received'), ('P', 'Pending')])),
      (
       b'file', models.CharField(max_length=255)),
      (
       b'headers', models.TextField(null=True)),
      (
       b'return_url', models.URLField(null=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Message', fields=[
      (
       b'message_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
      (
       b'headers', models.TextField(null=True)),
      (
       b'direction', models.CharField(max_length=5, choices=[('IN', 'Inbound'), ('OUT', 'Outbound')])),
      (
       b'timestamp', models.DateTimeField(auto_now_add=True)),
      (
       b'status', models.CharField(max_length=2, choices=[('S', 'Success'), ('E', 'Error'), ('W', 'Warning'), ('P', 'Pending'), ('IP', 'In Process')])),
      (
       b'adv_status', models.CharField(max_length=255, null=True)),
      (
       b'mic', models.CharField(max_length=100, null=True)),
      (
       b'mdn_mode', models.CharField(max_length=2, null=True, choices=[('SYNC', 'Synchronous'), ('ASYNC', 'Asynchronous')])),
      (
       b'mdn', models.OneToOneField(related_name=b'omessage', null=True, to=b'pyas2.MDN'))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Organization', fields=[
      (
       b'name', models.CharField(max_length=100)),
      (
       b'as2_name', models.CharField(max_length=100, serialize=False, primary_key=True)),
      (
       b'email_address', models.EmailField(max_length=75, null=True, blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Partner', fields=[
      (
       b'name', models.CharField(max_length=100)),
      (
       b'as2_name', models.CharField(max_length=100, serialize=False, primary_key=True)),
      (
       b'http_auth', models.BooleanField(default=False, verbose_name=b'HTTP Authentication')),
      (
       b'http_auth_user', models.CharField(max_length=100, null=True, blank=True)),
      (
       b'http_auth_pass', models.CharField(max_length=100, null=True, blank=True)),
      (
       b'target_url', models.URLField()),
      (
       b'subject', models.CharField(default=b'EDI Message sent using pyas2', max_length=255)),
      (
       b'content_type', models.CharField(default=b'application/edi-consent', max_length=100, choices=[('application/EDI-X12', 'application/EDI-X12'), ('application/EDIFACT', 'application/EDIFACT'), ('application/edi-consent', 'application/edi-consent'), ('application/XML', 'application/XML')])),
      (
       b'encryption', models.CharField(blank=True, max_length=20, null=True, choices=[('des_ede3_cbc', '3DES'), ('des_ede_cbc', 'DES'), ('rc2_40_cbc', 'RC2-40'), ('rc4', 'RC4-40'), ('aes_128_cbc', 'AES-128'), ('aes_192_cbc', 'AES-192'), ('aes_256_cbc', 'AES-256')])),
      (
       b'signature', models.CharField(blank=True, max_length=20, null=True, choices=[('sha1', 'SHA-1')])),
      (
       b'mdn', models.BooleanField(default=True, verbose_name=b'Request MDN')),
      (
       b'mdn_mode', models.CharField(default=b'SYNC', max_length=20, choices=[('SYNC', 'Synchronous'), ('ASYNC', 'Asynchronous')])),
      (
       b'mdn_sign', models.BooleanField(default=False, verbose_name=b'Request Signed MDN'))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Payload', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=100)),
      (
       b'content_type', models.CharField(max_length=255)),
      (
       b'file', models.CharField(max_length=255))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'PrivateCertificate', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'certificate', models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/djproject'), upload_to=b'certificates')),
      (
       b'ca_cert', models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/djproject'), null=True, upload_to=b'certificates', blank=True)),
      (
       b'certificate_passphrase', models.CharField(max_length=100))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'PublicCertificate', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'certificate', models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/djproject'), upload_to=b'certificates')),
      (
       b'ca_cert', models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/djproject'), null=True, upload_to=b'certificates', blank=True))], options={}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'partner', name=b'encryption_key', field=models.ForeignKey(related_name=b'enc_partner', blank=True, to=b'pyas2.PublicCertificate', null=True), preserve_default=True),
     migrations.AddField(model_name=b'partner', name=b'signature_key', field=models.ForeignKey(related_name=b'sign_partner', blank=True, to=b'pyas2.PublicCertificate', null=True), preserve_default=True),
     migrations.AddField(model_name=b'organization', name=b'encryption_key', field=models.ForeignKey(related_name=b'enc_org', blank=True, to=b'pyas2.PrivateCertificate', null=True), preserve_default=True),
     migrations.AddField(model_name=b'organization', name=b'signature_key', field=models.ForeignKey(related_name=b'sign_org', blank=True, to=b'pyas2.PrivateCertificate', null=True), preserve_default=True),
     migrations.AddField(model_name=b'message', name=b'organization', field=models.ForeignKey(to=b'pyas2.Organization', null=True), preserve_default=True),
     migrations.AddField(model_name=b'message', name=b'partner', field=models.ForeignKey(to=b'pyas2.Partner', null=True), preserve_default=True),
     migrations.AddField(model_name=b'message', name=b'payload', field=models.OneToOneField(related_name=b'message', null=True, to=b'pyas2.Payload'), preserve_default=True),
     migrations.AddField(model_name=b'log', name=b'message', field=models.ForeignKey(to=b'pyas2.Message'), preserve_default=True)]