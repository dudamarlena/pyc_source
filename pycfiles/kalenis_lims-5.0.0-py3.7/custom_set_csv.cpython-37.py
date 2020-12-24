# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_instrument_custom_set/custom_set_csv.py
# Compiled at: 2019-01-16 09:41:20
# Size of source mod 2**32: 608 bytes
import io, csv
from trytond.transaction import Transaction

def getControllerName():
    if Transaction().language in ('es', 'es_419'):
        return 'Planilla personalizada - CSV'
    return 'Custom Set - CSV'


def parse(self, infile):
    filedata = io.StringIO(infile)
    reader = csv.reader(filedata)
    for line in reader:
        print(str(', '.join(line), 'utf-8'))