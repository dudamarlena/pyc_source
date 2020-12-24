# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kula/workspace/ralph_pricing/src/ralph_pricing/tests/utils.py
# Compiled at: 2014-05-30 05:53:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import OrderedDict
import datetime
from decimal import Decimal as D
from ralph_pricing.models import DailyDevice, DailyExtraCost, Device, ExtraCostType, Venture

def get_or_create_device(name=None, asset_id=None, **kwargs):
    asset_id = asset_id if asset_id else Device.objects.all().count()
    name = name if name else (b'Default{0}').format(asset_id)
    return Device.objects.get_or_create(name=name, asset_id=asset_id, defaults=kwargs)[0]


def get_or_create_venture(name=None, venture_id=None, is_active=True, **kwargs):
    venture_id = venture_id if venture_id else Venture.objects.all().count()
    name = name if name else (b'Default{0}').format(venture_id)
    return Venture.objects.get_or_create(name=name, venture_id=venture_id, is_active=is_active, defaults=kwargs)[0]


def get_or_create_dailydevice(date, device, venture, **kwargs):
    return DailyDevice.objects.get_or_create(date=date, pricing_device=device, pricing_venture=venture, **kwargs)[0]


def get_or_create_extra_cost_type(name=None):
    if not name:
        name = (b'Default{0}').format(ExtraCostType.objects.all().count())
    return ExtraCostType.objects.get_or_create(name=name)[0]


def get_or_create_daily_extra_cost(date=None, venture=None, type=None, value=None):
    date = date if date else datetime.date(year=2014, month=5, day=1)
    venture = venture if venture else get_or_create_venture()
    type = type if type else get_or_create_extra_cost_type()
    value = value if value else D(100)
    return DailyExtraCost.objects.get_or_create(date=date, pricing_venture=venture, type=type, value=value)[0]


def sample_schema():
    return [
     OrderedDict([
      (
       b'field1', {b'name': b'Field1'}),
      (
       b'field2',
       {b'name': b'Field2', 
          b'currency': True, 
          b'total_cost': True})]),
     OrderedDict([
      (
       b'field3', {b'name': b'Field3'}),
      (
       b'field4',
       {b'name': b'Field4', 
          b'currency': True, 
          b'total_cost': True})])]