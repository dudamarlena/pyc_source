# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jon/DMN/Scripts/django-rolodex/rolodex/migrations/0001_initial.py
# Compiled at: 2015-09-21 21:42:44
from __future__ import unicode_literals
from django.db import models, migrations
import taggit.managers, rolodex.models

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0002_auto_20150616_2121')]
    operations = [
     migrations.CreateModel(name=b'Contact', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'type', models.CharField(max_length=100, choices=[('email', 'email'), ('phone', 'phone'), ('link', 'link'), ('address', 'address')])),
      (
       b'contact', models.CharField(max_length=250, null=True, blank=True)),
      (
       b'notes', models.TextField(null=True, blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Document', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'doc', models.FileField(null=True, upload_to=rolodex.models.upload_doc_directory, blank=True)),
      (
       b'link', models.URLField(null=True, blank=True)),
      (
       b'notes', models.TextField(null=True, blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'OpenRecordsLaw', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug', models.SlugField(unique=True, editable=False)),
      (
       b'name', models.CharField(max_length=250)),
      (
       b'link', models.URLField(null=True, blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Org', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug', models.SlugField(unique=True, editable=False)),
      (
       b'orgName', models.CharField(max_length=200)),
      (
       b'notes', models.TextField(null=True, blank=True)),
      (
       b'last_edited_by', models.CharField(max_length=250, null=True, blank=True)),
      (
       b'openRecordsLaw', models.ForeignKey(blank=True, to=b'rolodex.OpenRecordsLaw', null=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Org2Org', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'from_date', models.DateField(null=True, blank=True)),
      (
       b'to_date', models.DateField(null=True, blank=True)),
      (
       b'description', models.TextField(null=True, blank=True)),
      (
       b'hierarchy', models.CharField(default=b'none', max_length=10, choices=[('parent', 'parent'), ('child', 'child'), ('none', 'none')])),
      (
       b'from_ent', models.ForeignKey(related_name=b'org_from_org', to=b'rolodex.Org'))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Org2Org_Type', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug', models.SlugField(unique=True, editable=False)),
      (
       b'relationship_type', models.CharField(max_length=250))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Org2P', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'from_date', models.DateField(null=True, blank=True)),
      (
       b'to_date', models.DateField(null=True, blank=True)),
      (
       b'description', models.TextField(null=True, blank=True)),
      (
       b'from_ent', models.ForeignKey(related_name=b'p_from_org', to=b'rolodex.Org'))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'OrgContactRole', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug', models.SlugField(unique=True, editable=False)),
      (
       b'role', models.CharField(max_length=250)),
      (
       b'description', models.TextField(null=True, blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'P2Org', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'from_date', models.DateField(null=True, blank=True)),
      (
       b'to_date', models.DateField(null=True, blank=True)),
      (
       b'description', models.TextField(null=True, blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'P2Org_Type', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug', models.SlugField(unique=True, editable=False)),
      (
       b'relationship_type', models.CharField(max_length=250))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'P2P', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'from_date', models.DateField(null=True, blank=True)),
      (
       b'to_date', models.DateField(null=True, blank=True)),
      (
       b'description', models.TextField(null=True, blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'P2P_Type', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug', models.SlugField(unique=True, editable=False)),
      (
       b'relationship_type', models.CharField(max_length=250))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Person', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug', models.SlugField(unique=True, editable=False)),
      (
       b'lastName', models.CharField(max_length=100)),
      (
       b'firstName', models.CharField(max_length=100)),
      (
       b'position', models.CharField(max_length=250, null=True, blank=True)),
      (
       b'department', models.CharField(max_length=250, null=True, blank=True)),
      (
       b'gender', models.CharField(blank=True, max_length=250, null=True, choices=[('Female', 'Female'), ('Male', 'Male'), ('Other', 'Other')])),
      (
       b'birthdate', models.CharField(max_length=50, null=True, blank=True)),
      (
       b'race', models.CharField(blank=True, max_length=250, null=True, choices=[('White', 'White'), ('Black', 'Black'), ('American Indian', 'American Indian'), ('Asian', 'Asian'), ('Native Hawaiian and other Pacific Islander', 'Native Hawaiian and other Pacific Islander'), ('Other', 'Other'), ('Two or more races', 'Two or more races')])),
      (
       b'ethnicity', models.CharField(blank=True, max_length=250, null=True, choices=[('Hispanic', 'Hispanic'), ('Non-Hispanic', 'Non-Hispanic')])),
      (
       b'notes', models.TextField(null=True, blank=True)),
      (
       b'last_edited_by', models.CharField(max_length=250, null=True, blank=True)),
      (
       b'org_relations', models.ManyToManyField(related_name=b'people', through=b'rolodex.P2Org', to=b'rolodex.Org', blank=True)),
      (
       b'p_relations', models.ManyToManyField(related_name=b'+', through=b'rolodex.P2P', to=b'rolodex.Person', blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'PersonRole', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug', models.SlugField(unique=True, editable=False)),
      (
       b'role', models.CharField(max_length=250)),
      (
       b'description', models.TextField(null=True, blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'SearchLog', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'user', models.CharField(max_length=250)),
      (
       b'datestamp', models.DateField(auto_now=True)),
      (
       b'org', models.ForeignKey(related_name=b'org_log', blank=True, editable=False, to=b'rolodex.Org', null=True)),
      (
       b'person', models.ForeignKey(related_name=b'person_log', blank=True, editable=False, to=b'rolodex.Person', null=True))], options={}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'person', name=b'role', field=models.ForeignKey(related_name=b'person_role', blank=True, to=b'rolodex.PersonRole', null=True), preserve_default=True),
     migrations.AddField(model_name=b'person', name=b'tags', field=taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', help_text=b'A comma-separated list of tags.', verbose_name=b'Tags'), preserve_default=True),
     migrations.AddField(model_name=b'p2p', name=b'from_ent', field=models.ForeignKey(related_name=b'p_from_p', to=b'rolodex.Person'), preserve_default=True),
     migrations.AddField(model_name=b'p2p', name=b'relation', field=models.ForeignKey(related_name=b'p2p_relation', blank=True, to=b'rolodex.P2P_Type', null=True), preserve_default=True),
     migrations.AddField(model_name=b'p2p', name=b'to_ent', field=models.ForeignKey(related_name=b'p_to_p', to=b'rolodex.Person'), preserve_default=True),
     migrations.AddField(model_name=b'p2org', name=b'from_ent', field=models.ForeignKey(related_name=b'org_from_p', to=b'rolodex.Person'), preserve_default=True),
     migrations.AddField(model_name=b'p2org', name=b'relation', field=models.ForeignKey(related_name=b'p2org_relation', blank=True, to=b'rolodex.P2Org_Type', null=True), preserve_default=True),
     migrations.AddField(model_name=b'p2org', name=b'to_ent', field=models.ForeignKey(related_name=b'p_to_org', to=b'rolodex.Org'), preserve_default=True),
     migrations.AddField(model_name=b'org2p', name=b'relation', field=models.ForeignKey(related_name=b'org2p_relation', blank=True, to=b'rolodex.P2Org_Type', null=True), preserve_default=True),
     migrations.AddField(model_name=b'org2p', name=b'to_ent', field=models.ForeignKey(related_name=b'org_to_p', to=b'rolodex.Person'), preserve_default=True),
     migrations.AddField(model_name=b'org2org', name=b'relation', field=models.ForeignKey(related_name=b'org2org_relation', blank=True, to=b'rolodex.Org2Org_Type', null=True), preserve_default=True),
     migrations.AddField(model_name=b'org2org', name=b'to_ent', field=models.ForeignKey(related_name=b'org_to_org', to=b'rolodex.Org'), preserve_default=True),
     migrations.AddField(model_name=b'org', name=b'org_relations', field=models.ManyToManyField(related_name=b'+', through=b'rolodex.Org2Org', to=b'rolodex.Org', blank=True), preserve_default=True),
     migrations.AddField(model_name=b'org', name=b'p_relations', field=models.ManyToManyField(related_name=b'orgs', through=b'rolodex.Org2P', to=b'rolodex.Person', blank=True), preserve_default=True),
     migrations.AddField(model_name=b'org', name=b'tags', field=taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', help_text=b'A comma-separated list of tags.', verbose_name=b'Tags'), preserve_default=True),
     migrations.AddField(model_name=b'document', name=b'org', field=models.ForeignKey(related_name=b'org_doc', blank=True, to=b'rolodex.Org', null=True), preserve_default=True),
     migrations.AddField(model_name=b'document', name=b'person', field=models.ForeignKey(related_name=b'person_doc', blank=True, to=b'rolodex.Person', null=True), preserve_default=True),
     migrations.AddField(model_name=b'contact', name=b'org', field=models.ForeignKey(related_name=b'org_contact', blank=True, editable=False, to=b'rolodex.Org', null=True), preserve_default=True),
     migrations.AddField(model_name=b'contact', name=b'person', field=models.ForeignKey(related_name=b'person_contact', blank=True, editable=False, to=b'rolodex.Person', null=True), preserve_default=True),
     migrations.AddField(model_name=b'contact', name=b'role', field=models.ForeignKey(blank=True, to=b'rolodex.OrgContactRole', null=True), preserve_default=True)]