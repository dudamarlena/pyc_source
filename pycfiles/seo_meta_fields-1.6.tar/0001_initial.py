# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/himanshubansal/Desktop/meta_management/meta_fields/migrations/0001_initial.py
# Compiled at: 2017-02-23 08:51:10
from __future__ import unicode_literals
from django.db import migrations, models
import multiselectfield.db.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'AdvancedTags', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'meta_robot', multiselectfield.db.fields.MultiSelectField(choices=[('Allow search engines to index this page (assumed).', 'Allow search engines to index this page (assumed).'), ('Allow search engines to follow links on this page (assumed).', 'Allow search engines to follow links on this page (assumed).'), ('Prevents search engines from indexing this page.', 'Prevents search engines from indexing this page.'), ('Prevents search engines from following links on this page.', 'Prevents search engines from following links on this page.'), ('Prevents cached copies of this page from appearing in search results.', 'Prevents cached copies of this page from appearing in search results.'), ('Prevents descriptions from appearing in search results, and prevents page caching.',
 'Prevents descriptions from appearing in search results, and prevents page caching.'), ('Blocks the Open Directory Project description from appearing in search results.',
 'Blocks the Open Directory Project description from appearing in search results.'), ('Prevents Yahoo! from listing this page in the Yahoo! Directory.', 'Prevents Yahoo! from listing this page in the Yahoo! Directory.'), ('Prevent search engines from indexing images on this page.', 'Prevent search engines from indexing images on this page.'), ('Prevent search engines from offering to translate this page in search results.',
 'Prevent search engines from offering to translate this page in search results.'), ('Provides search engines with specific directions for what to do when this page is indexed.',
 'Provides search engines with specific directions for what to do when this page is indexed.')], max_length=255)),
      (
       b'news_keywords', models.CharField(max_length=255)),
      (
       b'standout', models.CharField(max_length=255)),
      (
       b'content_rating', models.CharField(choices=[('none', 'None'), ('general', 'General'), ('mature', 'Mature'), ('restricted', 'Restricted'), ('14 years or older', '14 years or older'), ('safe for kids', 'Safe for kids')], max_length=255)),
      (
       b'referrer_policy', models.CharField(choices=[('none', 'None'), ('no referrer', 'No Referrer'), ('origin', 'Origin'), ('No Refrerer when downgrade', 'No Refrerer when downgrade'), ('origin when cross origin', 'Origin when cross origin'), ('unsafe url', 'Unsafe Url')], max_length=255)),
      (
       b'generator', models.CharField(max_length=255)),
      (
       b'rights', models.CharField(max_length=255)),
      (
       b'image', models.ImageField(max_length=255, upload_to=b'')),
      (
       b'shortlink_url', models.CharField(max_length=255)),
      (
       b'original_source', models.CharField(max_length=255)),
      (
       b'previous_page_url', models.CharField(max_length=255)),
      (
       b'next_page_url', models.CharField(max_length=255)),
      (
       b'content_language', models.CharField(max_length=255)),
      (
       b'geo_position', models.CharField(max_length=255)),
      (
       b'geo_place_name', models.CharField(max_length=255)),
      (
       b'geo_region', models.CharField(max_length=255)),
      (
       b'icbm', models.CharField(max_length=255)),
      (
       b'refresh', models.CharField(max_length=255)),
      (
       b'revisit_after_interval', models.CharField(choices=[('none', 'None'), ('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], max_length=255)),
      (
       b'pragma', models.CharField(max_length=255)),
      (
       b'cache_control', models.CharField(max_length=255)),
      (
       b'expires', models.CharField(max_length=255))]),
     migrations.CreateModel(name=b'BasicTags', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'meta_title', models.CharField(max_length=255)),
      (
       b'meta_description', models.TextField()),
      (
       b'meta_keywords', models.TextField())]),
     migrations.CreateModel(name=b'BingVerification', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'meta_tag', models.CharField(max_length=255)),
      (
       b'file_upload', models.FileField(upload_to=b'')),
      (
       b'verification_file', models.CharField(max_length=255)),
      (
       b'verification_file_content', models.CharField(max_length=255))]),
     migrations.CreateModel(name=b'GoogleVerification', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'meta_tag', models.CharField(max_length=255)),
      (
       b'file_upload', models.FileField(upload_to=b'')),
      (
       b'verification_file', models.CharField(max_length=255)),
      (
       b'verification_file_content', models.CharField(max_length=255))]),
     migrations.CreateModel(name=b'MetaImage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'image_alt', models.CharField(max_length=255)),
      (
       b'image_title', models.CharField(max_length=255)),
      (
       b'image_url', models.CharField(max_length=255))]),
     migrations.CreateModel(name=b'OpenGraph', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'site_name', models.CharField(max_length=255)),
      (
       b'content_type', models.CharField(max_length=255)),
      (
       b'page_url', models.CharField(max_length=255)),
      (
       b'content_title', models.CharField(max_length=255)),
      (
       b'content_description', models.TextField()),
      (
       b'content_title_determiner', models.CharField(choices=[('ignore', 'Ignore'), ('automatic', 'Automatic'), ('an', 'An'), ('a', 'A'), ('the', 'The')], max_length=255)),
      (
       b'content_modification_date_time', models.DateTimeField()),
      (
       b'see_also', models.CharField(max_length=255)),
      (
       b'image', models.ImageField(help_text=b'Image for OpenGraph', upload_to=b'')),
      (
       b'image_url', models.CharField(max_length=255)),
      (
       b'secure_image_url', models.CharField(max_length=255)),
      (
       b'image_type', models.CharField(max_length=255)),
      (
       b'image_width', models.CharField(max_length=255)),
      (
       b'image_height', models.CharField(max_length=255)),
      (
       b'logitude', models.CharField(max_length=255)),
      (
       b'latitude', models.CharField(max_length=255)),
      (
       b'street_number', models.CharField(max_length=255)),
      (
       b'locality', models.CharField(max_length=255)),
      (
       b'region', models.CharField(max_length=255)),
      (
       b'zip_code', models.CharField(max_length=255)),
      (
       b'email', models.EmailField(max_length=255)),
      (
       b'phone_number', models.CharField(max_length=255)),
      (
       b'fax_number', models.CharField(max_length=255))]),
     migrations.CreateModel(name=b'SiteInformation', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'site_name', models.CharField(max_length=255)),
      (
       b'site_slogan', models.CharField(max_length=255)),
      (
       b'email_id', models.CharField(max_length=255)),
      (
       b'logo_image_alt_text', models.CharField(max_length=255))])]