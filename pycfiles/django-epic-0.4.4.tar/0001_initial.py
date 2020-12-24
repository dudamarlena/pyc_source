# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidm/egauge/web/www/django/egauge_django/epic/migrations/0001_initial.py
# Compiled at: 2015-01-20 21:47:45
from __future__ import unicode_literals
from django.db import models, migrations
from decimal import Decimal
import django.core.validators

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Assembly_Item', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'qty', models.PositiveIntegerField(help_text=b'The quantity of this component required by the assembly.')),
      (
       b'refdes', models.TextField(default=b'', help_text=b'A list of comma-separated reference designators e.g., "R101,R304". The length of this list should match Quantity.', verbose_name=b'Refdes List', blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Delta', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'is_absolute', models.BooleanField(default=False, help_text=b'If set, the adjustment is absolute otherwise it is relative.', verbose_name=b'Absolute Adjustment')),
      (
       b'adj', models.IntegerField(help_text=b'The amount by which the part quantity should be adjusted by.', verbose_name=b'Adjustment Count'))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Line_Item', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'qty', models.PositiveIntegerField(help_text=b'The quantity of this part.')),
      (
       b'line_cost', models.DecimalField(help_text=b'The total cost of this line-item.  Part-cost is line-item cost divided by quantity.', verbose_name=b'Amount', max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal(b'0.00'))])),
      (
       b'index', models.PositiveIntegerField(help_text=b'Sequential and unchanging index of this line-item.'))], options={b'ordering': [
                    b'index']}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Part', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'val', models.CharField(default=b'', help_text=b'The primary value of the part such as resistance for a resistor or capacitance for a capacitor.', max_length=31, verbose_name=b'Value', blank=True)),
      (
       b'descr', models.CharField(default=b'', help_text=b'Brief listing of key parameters of the part, such as temperature range, drift, max. voltages, etc.', max_length=127, verbose_name=b'Description', blank=True)),
      (
       b'footprint', models.CharField(default=b'', help_text=b"The part's PCB footprint.", max_length=63, blank=True)),
      (
       b'mfg', models.CharField(help_text=b'The name of the manufacturer of the part.', max_length=31, verbose_name=b'Manufacturer')),
      (
       b'mfg_pn', models.CharField(max_length=31, verbose_name=b"Manufacturer's Part #")),
      (
       b'mounting', models.IntegerField(default=0, help_text=b"How the part is mounted to a PCB (free if it's not mounted at all, such as a plug).", verbose_name=b'Mounting Type', choices=[(0, 'SMD'), (1, 'THD'), (2, 'chassis'), (3, 'free')])),
      (
       b'target_price', models.DecimalField(help_text=b'The expected price of the part.', verbose_name=b'Target price [$]', max_digits=10, decimal_places=6, validators=[django.core.validators.MinValueValidator(Decimal(b'0.000001'))])),
      (
       b'overage', models.DecimalField(help_text=b'Worst-case percentage of parts we expect to lose due to attrition at the assembly-house.', verbose_name=b'Overage [%]', max_digits=6, decimal_places=3, validators=[django.core.validators.MinValueValidator(Decimal(b'0')), django.core.validators.MaxValueValidator(Decimal(b'100'))])),
      (
       b'spq', models.IntegerField(default=1, help_text=b'The number of parts in a standard package.  For example, 10,000 pieces in a reel.', verbose_name=b'Standard-Package Qty')),
      (
       b'lead_time', models.PositiveIntegerField(help_text=b'Lead-time in weeks.', verbose_name=b'Lead-time [weeks]')),
      (
       b'status', models.IntegerField(default=0, help_text=b"The life-time status of this part. Parts marked `preview' and `obsolete' are not considered orderable.", verbose_name=b'Life-time Status', choices=[(0, 'preview'), (1, 'active'), (2, 'deprecated'), (3, 'obsolete')])),
      (
       b'substitute', models.ForeignKey(blank=True, to=b'epic.Part', help_text=b'List of other parts that are (identical) substitutes for this part.', null=True, verbose_name=b'Substitutes'))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Transaction', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'ts', models.DateTimeField(help_text=b'Date and time when this transaction was created.', verbose_name=b'Creation Time')),
      (
       b'notes', models.TextField(help_text=b'Comments and notes for this transaction', verbose_name=b'Notes', blank=True))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Shipment', fields=[
      (
       b'transaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'epic.Transaction')),
      (
       b'tracking', models.CharField(default=b'', help_text=b'Comma-separated list of tracking numbers.', max_length=127, verbose_name=b'Tracking #s', blank=True)),
      (
       b'cost_freight', models.DecimalField(verbose_name=b'Freight Cost', max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal(b'0.00'))])),
      (
       b'cost_other', models.DecimalField(help_text=b'Other costs assessed by the shipper, such as handling costs.', verbose_name=b'Other Costs', max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal(b'0.00'))])),
      (
       b'cost_discount', models.DecimalField(help_text=b'Discounts given by the shipper, such as early payment discount.', verbose_name=b'Discount Given', max_digits=9, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal(b'0.00'))]))], options={}, bases=('epic.transaction', )),
     migrations.CreateModel(name=b'Order', fields=[
      (
       b'transaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'epic.Transaction')),
      (
       b'expected_arrival_date', models.DateField(help_text=b'Date when the order is expected to arrive.', verbose_name=b'Expected Arrival Date')),
      (
       b'status', models.IntegerField(default=0, verbose_name=b'Order Status', choices=[(0, 'open'), (1, 'closed')]))], options={}, bases=('epic.transaction', )),
     migrations.CreateModel(name=b'Inventory', fields=[
      (
       b'transaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'epic.Transaction'))], options={}, bases=('epic.transaction', )),
     migrations.CreateModel(name=b'Vendor', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(unique=True, max_length=31, verbose_name=b'Vendor Name', db_index=True)),
      (
       b'search_url', models.CharField(default=b'', help_text=b"This pattern defines how to search for a particular part on the vendor's website.  %(vendor_pn)s gets replaced by the vendor's part-number, %(mfg)s by the manufacturer's name, and %(mfg_pn)s by the manufacturer's part-number.", max_length=127, verbose_name=b'Search URL Pattern', blank=True))], options={b'ordering': [
                    b'name']}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Vendor_Part', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'vendor_pn', models.CharField(max_length=31, verbose_name=b"Vendor's Part #")),
      (
       b'price', models.DecimalField(max_digits=10, decimal_places=6, validators=[django.core.validators.MinValueValidator(Decimal(b'0.000001'))])),
      (
       b'part', models.ForeignKey(verbose_name=b'Part #', to=b'epic.Part')),
      (
       b'vendor', models.ForeignKey(to=b'epic.Vendor'))], options={}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Warehouse', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(help_text=b'The name of the warehouse.', unique=True, max_length=31)),
      (
       b'address', models.TextField(default=b'', help_text=b'The shipping address for the warehouse.', blank=True))], options={b'ordering': [
                    b'name']}, bases=(
      models.Model,)),
     migrations.AlterUniqueTogether(name=b'vendor_part', unique_together=set([('vendor', 'vendor_pn'), ('vendor', 'part')])),
     migrations.AddField(model_name=b'transaction', name=b'warehouse', field=models.ForeignKey(verbose_name=b'Warehouse', to=b'epic.Warehouse', help_text=b'The (destination) warehouse this transaction applies to.'), preserve_default=True),
     migrations.AddField(model_name=b'shipment', name=b'from_warehouse', field=models.ForeignKey(blank=True, to=b'epic.Warehouse', help_text=b'For an inter-warehouse shipment, the warehouse the shipment originates from.', null=True), preserve_default=True),
     migrations.AddField(model_name=b'shipment', name=b'ordr', field=models.ForeignKey(blank=True, to=b'epic.Order', help_text=b'For an order shipment, the order that resulted in this shipment.', null=True, verbose_name=b'Order #'), preserve_default=True),
     migrations.AlterUniqueTogether(name=b'part', unique_together=set([('mfg', 'mfg_pn')])),
     migrations.AlterIndexTogether(name=b'part', index_together=set([('mfg', 'mfg_pn')])),
     migrations.AddField(model_name=b'order', name=b'vendor', field=models.ForeignKey(help_text=b'The name of the vendor (distributor) where the order was placed.', to=b'epic.Vendor'), preserve_default=True),
     migrations.AddField(model_name=b'line_item', name=b'part', field=models.ForeignKey(verbose_name=b'Part #', to=b'epic.Part'), preserve_default=True),
     migrations.AddField(model_name=b'line_item', name=b'txtn', field=models.ForeignKey(verbose_name=b'Transaction #', to=b'epic.Transaction'), preserve_default=True),
     migrations.AlterUniqueTogether(name=b'line_item', unique_together=set([('txtn', 'part'), ('txtn', 'index')])),
     migrations.AlterIndexTogether(name=b'line_item', index_together=set([('txtn', 'part')])),
     migrations.AddField(model_name=b'delta', name=b'part', field=models.ForeignKey(verbose_name=b'Part #', to=b'epic.Part', help_text=b'The part whose quantity gets adjusted.'), preserve_default=True),
     migrations.AddField(model_name=b'delta', name=b'txtn', field=models.ForeignKey(verbose_name=b'Transaction #', to=b'epic.Transaction'), preserve_default=True),
     migrations.AddField(model_name=b'delta', name=b'warehouse', field=models.ForeignKey(to=b'epic.Warehouse'), preserve_default=True),
     migrations.AddField(model_name=b'assembly_item', name=b'assy', field=models.ForeignKey(related_name=b'assembly_item_part', verbose_name=b'Assembly Part #', to=b'epic.Part', help_text=b'The part number of the assembly this item belongs to.'), preserve_default=True),
     migrations.AddField(model_name=b'assembly_item', name=b'comp', field=models.ForeignKey(related_name=b'assembly_item_comp', verbose_name=b'Component Part #', to=b'epic.Part', help_text=b'The part number of the component of this item.'), preserve_default=True),
     migrations.AlterUniqueTogether(name=b'assembly_item', unique_together=set([('assy', 'comp')])),
     migrations.AlterIndexTogether(name=b'assembly_item', index_together=set([('assy', 'comp')]))]