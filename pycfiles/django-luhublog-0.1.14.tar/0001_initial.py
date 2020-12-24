# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johsanca/Projects/luhu-blog-app/luhublog/migrations/0001_initial.py
# Compiled at: 2015-10-22 12:12:03
from __future__ import unicode_literals
from django.db import migrations, models
import sorl.thumbnail.fields, model_utils.fields, froala_editor.fields, luhublog.models.entry, django.utils.timezone
from django.conf import settings
import taggit.managers

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0002_auto_20150616_2121'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('sites', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Author', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'name', models.CharField(default=b'', max_length=200, verbose_name=b'Nombre / seudónimo del autor', blank=True)),
      (
       b'headline', models.CharField(default=b'', max_length=255, verbose_name=b'Corta descripción', blank=True)),
      (
       b'twitter', models.CharField(default=b'', help_text=b'@EsLuhu', max_length=50, verbose_name=b'Twitter', blank=True)),
      (
       b'facebook_page_url', models.URLField(verbose_name=b'URL Pagina Facebook', blank=True)),
      (
       b'twitter_url', models.URLField(verbose_name=b'URL Perfil Facebook', blank=True)),
      (
       b'google_plus_url', models.URLField(verbose_name=b'URL Perfil Google Plus', blank=True)),
      (
       b'is_active', models.BooleanField(default=True, verbose_name=b'is active')),
      (
       b'user', models.OneToOneField(related_name=b'weblog_author', verbose_name=b'Perfil de usuario', to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created'], 
        b'verbose_name': b'Autor', 
        b'verbose_name_plural': b'Autores'}),
     migrations.CreateModel(name=b'Blog', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'title', models.CharField(max_length=60, verbose_name=b'Nombre del blog')),
      (
       b'tag_line', models.CharField(max_length=140, verbose_name=b'Descripción del blog')),
      (
       b'entries_per_page', models.IntegerField(default=10, verbose_name=b'Entradas por pagina')),
      (
       b'recents', models.IntegerField(default=5, verbose_name=b'Numero de entradas recientes a mostrar')),
      (
       b'site', models.OneToOneField(verbose_name=b'Site', to=b'sites.Site'))], options={b'abstract': False}),
     migrations.CreateModel(name=b'BlogSocialMedia', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'facebook', models.URLField(verbose_name=b'Facebook URL', blank=True)),
      (
       b'twitter', models.URLField(verbose_name=b'Twitter URL', blank=True)),
      (
       b'google_plus', models.URLField(verbose_name=b'Google plus URL', blank=True)),
      (
       b'instagram', models.URLField(verbose_name=b'Instagram URL', blank=True)),
      (
       b'linkedin', models.URLField(verbose_name=b'Linkedin URL', blank=True)),
      (
       b'youtube', models.URLField(verbose_name=b'YouTube URL', blank=True)),
      (
       b'pinterest', models.URLField(verbose_name=b'Pinterest URL', blank=True)),
      (
       b'blog', models.OneToOneField(related_name=b'social_media', verbose_name=b'Blog', to=b'luhublog.Blog'))], options={b'verbose_name': b'Redes sociales de los blogs'}),
     migrations.CreateModel(name=b'Entry', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'title', models.CharField(max_length=100, verbose_name=b'title')),
      (
       b'slug', models.SlugField(help_text=b"Used to build the entry's URL.", unique=True, verbose_name=b'slug')),
      (
       b'lead_entry', models.CharField(max_length=255, verbose_name=b'Encabezado', blank=True)),
      (
       b'image_header', sorl.thumbnail.fields.ImageField(upload_to=luhublog.models.entry.rename_filename, null=True, verbose_name=b'Imagen de encabezado', blank=True)),
      (
       b'image_caption', sorl.thumbnail.fields.ImageField(upload_to=luhublog.models.entry.rename_filename, null=True, verbose_name=b'Imagen de la entrada', blank=True)),
      (
       b'content', froala_editor.fields.FroalaField(verbose_name=b'Cuerpo de la entrada')),
      (
       b'status', model_utils.fields.StatusField(default=b'DRAFT', max_length=100, no_check_for_status=True, choices=[('DRAFT', 'DRAFT'), ('HIDDEN', 'HIDDEN'), ('PUBLISHED', 'PUBLISHED')])),
      (
       b'start_publication', models.DateTimeField(db_index=True, null=True, verbose_name=b'Fecha de publicación', blank=True)),
      (
       b'seo_title', models.CharField(default=b'', help_text=b'Google typically displays the first 50-60 characters of a title tag', max_length=60, verbose_name=b'Meta Title', blank=True)),
      (
       b'seo_description', models.CharField(default=b'', help_text=b'The description should optimally be between 10-155 characters', max_length=155, verbose_name=b'Meta Description', blank=True)),
      (
       b'seo_keywords', models.CharField(default=b'', help_text=b'Opcional', max_length=400, verbose_name=b'Meta Keywords', blank=True)),
      (
       b'author', models.ForeignKey(related_name=b'entries', verbose_name=b'Autor de la entrada', to=b'luhublog.Author')),
      (
       b'blog', models.ForeignKey(blank=True, editable=False, to=b'luhublog.Blog', verbose_name=b'Site'))], options={b'ordering': [
                    b'-created'], 
        b'get_latest_by': b'-start_publication', 
        b'verbose_name': b'Entrada', 
        b'verbose_name_plural': b'Entradas'}),
     migrations.CreateModel(name=b'EntryCategory', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'name', models.CharField(max_length=60, verbose_name=b'Nombre')),
      (
       b'slug', models.SlugField(verbose_name=b'ULR Slug')),
      (
       b'description', models.CharField(max_length=255, verbose_name=b'Descripción', blank=True)),
      (
       b'image_cover', sorl.thumbnail.fields.ImageField(upload_to=luhublog.models.entry.rename_filename, null=True, verbose_name=b'Imagen de portada', blank=True)),
      (
       b'blog', models.ForeignKey(blank=True, editable=False, to=b'luhublog.Blog', verbose_name=b'Site')),
      (
       b'tags', taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', blank=True, help_text=b'A comma-separated list of tags.', verbose_name=b'Tags'))], options={b'verbose_name': b'Categoría', 
        b'verbose_name_plural': b'Categorías'}),
     migrations.CreateModel(name=b'OpenGraph', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'og_type', models.CharField(default=b'blog', max_length=255, verbose_name=b'Resource type', choices=[('article', 'Article'), ('website', 'Website'), ('blog', 'Blog'), ('book', 'Book'), ('game', 'Game'), ('movie', 'Movie'), ('food', 'Food'), ('city', 'City'), ('country', 'Country'), ('actor', 'Actor'), ('author', 'Author'), ('politician', 'Politician'), ('company', 'Company'), ('hotel', 'Hotel'), ('restaurant', 'Restaurant')])),
      (
       b'og_title', models.CharField(default=b'', help_text=b'titulo', max_length=255, verbose_name=b'Open Graph Title', blank=True)),
      (
       b'og_description', models.CharField(default=b'', help_text=b'Facebook can display up to 300 characters, but I suggest treating anything above 200 as something extra.', max_length=300, verbose_name=b'Open Graph Description', blank=True)),
      (
       b'og_app_id', models.CharField(default=b'', max_length=255, verbose_name=b'Facebook App ID', blank=True)),
      (
       b'og_image', sorl.thumbnail.fields.ImageField(help_text=b'Imagen de 1200px por 630px', upload_to=b'seo/opengraph/', verbose_name=b'twitter:site')),
      (
       b'object_id', models.PositiveIntegerField()),
      (
       b'content_type', models.ForeignKey(to=b'contenttypes.ContentType'))], options={b'verbose_name': b'Social Metadata'}),
     migrations.CreateModel(name=b'TwitterCard', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=b'created', editable=False)),
      (
       b'modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=b'modified', editable=False)),
      (
       b'site', models.CharField(help_text=b'@empresa', max_length=30, verbose_name=b'twitter:site')),
      (
       b'creator', models.CharField(help_text=b'@autor', max_length=30, verbose_name=b'twitter:creator')),
      (
       b'title', models.CharField(help_text=b'Máximo 70 caracteres', max_length=70, verbose_name=b'twitter:title')),
      (
       b'description', models.CharField(help_text=b'Máximo 200 caracteres', max_length=200, verbose_name=b'twitter:description')),
      (
       b'image', sorl.thumbnail.fields.ImageField(help_text=b'Imagen de 280px por 150px', upload_to=b'seo/twitter_cards/', verbose_name=b'twitter:site')),
      (
       b'object_id', models.PositiveIntegerField()),
      (
       b'content_type', models.ForeignKey(to=b'contenttypes.ContentType'))], options={b'verbose_name': b'Twitter Card'}),
     migrations.AddField(model_name=b'entry', name=b'category', field=models.ForeignKey(verbose_name=b'Categoría', blank=True, to=b'luhublog.EntryCategory', null=True)),
     migrations.AddField(model_name=b'entry', name=b'related', field=models.ManyToManyField(related_name=b'_related_+', verbose_name=b'related entries', to=b'luhublog.Entry', blank=True)),
     migrations.AddField(model_name=b'entry', name=b'tags', field=taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', blank=True, help_text=b'A comma-separated list of tags.', verbose_name=b'Tags')),
     migrations.AlterIndexTogether(name=b'entry', index_together=set([('slug', 'created'), ('status', 'created', 'start_publication')]))]