# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/maxipago/utils/payment_processors.py
# Compiled at: 2018-07-08 23:37:16
# Size of source mod 2**32: 359 bytes
TEST, REDECARD, AMEX, CIELO, TEF, CHASEPAYMENTECH, BSITAU, BSBRADESCO = ('1', '2',
                                                                         '3', '4',
                                                                         '5', '8',
                                                                         '11', '12')
PROCESSORS_CHOICES = (
 (
  TEST, 'Simulador de testes'),
 (
  REDECARD, 'Redecard'),
 (
  AMEX, 'Amex'),
 (
  CIELO, 'Cielo'),
 (
  TEF, 'TEF'),
 (
  CHASEPAYMENTECH, 'ChasePaymentech'),
 (
  BSITAU, 'BSItau'),
 (
  BSBRADESCO, 'BSBradesco'))