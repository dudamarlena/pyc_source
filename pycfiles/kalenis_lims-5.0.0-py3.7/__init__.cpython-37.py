# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_sale/__init__.py
# Compiled at: 2018-05-23 18:06:03
# Size of source mod 2**32: 445 bytes
from trytond.pool import Pool
from . import sale

def register():
    Pool.register((sale.Sale),
      (sale.SaleLoadServicesStart),
      module='lims_sale',
      type_='model')
    Pool.register((sale.SaleLoadServices),
      module='lims_sale',
      type_='wizard')