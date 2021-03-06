# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0011_auto_20170720_1945.py
# Compiled at: 2018-03-26 19:55:27
# Size of source mod 2**32: 3189 bytes
from __future__ import unicode_literals
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('core', '0010_auto_20170720_1643')]
    operations = [
     migrations.CreateModel(name='PaymentRecord', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'creationDate', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'modifiedDate', models.DateTimeField(auto_now=True, verbose_name='Last updated'))], options={'verbose_name': 'Payment record', 
      'verbose_name_plural': 'Payment records'}),
     migrations.CreateModel(name='CashPaymentRecord', fields=[
      (
       'paymentrecord_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.PaymentRecord')),
      (
       'amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount paid')),
      (
       'payerEmail', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Payer email')),
      (
       'status', models.CharField(choices=[('N', 'Cash payment recorded, needs collection'), ('C', 'Cash payment collected'), ('R', 'Refunded in full')], default='N', max_length=1, verbose_name='Payment status')),
      (
       'collectedByUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collectedcashpayments', to=settings.AUTH_USER_MODEL, verbose_name='Collected by user'))], options={'verbose_name': 'Cash payment record', 
      'verbose_name_plural': 'Cash payment records'}, bases=('core.paymentrecord', )),
     migrations.AddField(model_name='paymentrecord', name='invoice', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Invoice', verbose_name='Invoice')),
     migrations.AddField(model_name='paymentrecord', name='polymorphic_ctype', field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_core.paymentrecord_set+', to='contenttypes.ContentType')),
     migrations.AddField(model_name='paymentrecord', name='submissionUser', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_submitted', to=settings.AUTH_USER_MODEL, verbose_name='Submission user'))]