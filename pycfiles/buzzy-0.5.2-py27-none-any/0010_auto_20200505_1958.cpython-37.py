# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0010_auto_20200505_1958.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 1063 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('explore', '0009_auto_20200420_1521')]
    operations = [
     migrations.AlterField(model_name='corpus',
       name='language',
       field=models.ForeignKey(choices=[
      ('benepar_ar', 'ar'),
      ('benepar_de', 'de'),
      ('benepar_en_small', 'en'),
      ('benepar_eu', 'eu'),
      ('benepar_fr', 'fr'),
      ('benepar_he', 'he'),
      ('benepar_hu', 'hu'),
      ('benepar_ko', 'ko'),
      ('benepar_pl', 'pl'),
      ('benepar_sv', 'sv'),
      ('benepar_zh', 'zh')],
       null=True,
       on_delete=(django.db.models.deletion.SET_NULL),
       to='explore.Language'))]