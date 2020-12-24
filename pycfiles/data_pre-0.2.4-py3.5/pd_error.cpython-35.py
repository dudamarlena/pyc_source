# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pre/pd_error.py
# Compiled at: 2019-06-25 04:51:43
# Size of source mod 2**32: 699 bytes
"""
@author: magician
@file: excel.py
@date: 2018/12/21
"""
HCPoChecker = {'Order No.': str, 
 'Year': int, 
 'Planning Ssn': str, 
 'Item Brand': str, 
 'Transportation Method': str, 
 'Payment Terms': str, 
 'Payment Currency': str, 
 'Order Plan Number': int, 
 'Item Code': str, 
 'Contracted ETD': 'datetime', 
 'ETA WH': 'datetime', 
 'Management Factory Code': str, 
 'Management Factory': str, 
 'Branch Factory Code': str, 
 'Branch Factory': str, 
 'Color Code': int, 
 'Color': str, 
 'Size Code': int, 
 'Size': str, 
 'SKU Code': int, 
 'Sample Code': str, 
 'Order Qty(pcs)': int}
checker = {'hc_po': HCPoChecker}