# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0017_cashdiary_cashmovement.py
# Compiled at: 2018-04-06 07:48:01
# Size of source mod 2**32: 5515 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('codenerix_pos', '0001_initial'),
     ('codenerix_invoicing', '0016_purchaseslinealbaran_product_unique')]
    operations = [
     migrations.CreateModel(name='CashDiary', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'opened_date', models.DateTimeField(verbose_name='Opened Date')),
      (
       'opened_cash', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Opened Cash')),
      (
       'opened_cash_extra', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Opened Cash Deviation')),
      (
       'opened_cash_notes', models.TextField(blank=True, default='', verbose_name='Opened Cash Notes')),
      (
       'opened_cards', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Opened Cards')),
      (
       'opened_cards_extra', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Opened Cards Deviation')),
      (
       'opened_cards_notes', models.TextField(blank=True, default='', verbose_name='Opened Cards Notes')),
      (
       'closed_date', models.DateTimeField(blank=True, null=True, verbose_name='Closed Date')),
      (
       'closed_cash', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Closed Cash')),
      (
       'closed_cash_extra', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Closed Cash Deviation')),
      (
       'closed_cash_notes', models.TextField(blank=True, default='', verbose_name='Closed Cash Notes')),
      (
       'closed_cards', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Closed Cards')),
      (
       'closed_cards_extra', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Closed Cards Deviation')),
      (
       'closed_cards_notes', models.TextField(blank=True, default='', verbose_name='Closed Cards Notes')),
      (
       'closed_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='closed_cash_diarys', to=settings.AUTH_USER_MODEL, verbose_name='User')),
      (
       'opened_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opened_cash_diarys', to=settings.AUTH_USER_MODEL, verbose_name='User')),
      (
       'pos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_movements', to='codenerix_pos.POS', verbose_name='Point of Sales'))], options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 
      'abstract': False}),
     migrations.CreateModel(name='CashMovement', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'kind', models.CharField(choices=[('TRA', 'Wire transfer'), ('CAR', 'Card'), ('CAS', 'Cash'), ('CRE', 'Credit'), ('PYP', 'Paypal'), ('30C', '30 day credit'), ('60C', '60 day credit'), ('90C', '90 day credit')], max_length=3, verbose_name='Kind')),
      (
       'kind_card', models.CharField(blank=True, choices=[('VIS', 'Visa'), ('MAS', 'MasterCard'), ('AME', 'American Express'), ('OTH', 'Other')], max_length=3, null=True, verbose_name='Kind Card')),
      (
       'date_movement', models.DateTimeField(verbose_name='Date of movement')),
      (
       'amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
      (
       'reason', models.TextField(blank=True, default=None, null=True, verbose_name='Reason')),
      (
       'cash_diary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_movements', to='codenerix_invoicing.CashDiary', verbose_name='Cash diary')),
      (
       'order', models.ManyToManyField(related_name='cash_movements', to='codenerix_invoicing.SalesOrder', verbose_name='Sales orders')),
      (
       'pos_slot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_movements', to='codenerix_pos.POSSlot', verbose_name='Slot')),
      (
       'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_movements', to=settings.AUTH_USER_MODEL, verbose_name='User'))], options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 
      'abstract': False})]