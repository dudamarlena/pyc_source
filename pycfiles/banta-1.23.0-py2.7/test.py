# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\optional\printer\test.py
# Compiled at: 2012-08-07 08:25:22
from packages.non_free.printer.hasarPrinter import HasarPrinter
print 'Usando driver de Hasar'
printer = HasarPrinter(deviceFile='/dev/ttyS0', model='615', dummy=True)
number = printer.getLastNumber('B') + 1
print 'imprimiendo la FC ', number
printer.openTicket()
printer.addItem('CARAMELOS', 1, 1.5, 21, discount=0, discountDescription='')
printer.addItem('CIGARRILLOS', 2, 10, 21, discount=0, discountDescription='')
printer.addPayment('Efectivo', 11.5)
printer.closeDocument()