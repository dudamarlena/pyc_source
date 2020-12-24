# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ecereto/src/pyboleto/tests/test_banco_do_brasil.py
# Compiled at: 2016-04-10 23:42:52
# Size of source mod 2**32: 1202 bytes
import unittest, datetime
from pyboleto.bank.bancodobrasil import BoletoBB
from .testutils import BoletoTestCase

class TestBancoBrasil(BoletoTestCase):

    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoBB(7, 1)
            d.carteira = '18'
            d.data_documento = datetime.date(2011, 3, 8)
            d.data_vencimento = datetime.date(2011, 3, 8)
            d.data_processamento = datetime.date(2012, 7, 4)
            d.valor_documento = 2952.95
            d.agencia = '9999'
            d.conta = '99999'
            d.convenio = '7777777'
            d.nosso_numero = str(87654 + i)
            d.numero_documento = str(87654 + i)
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(self.dados[0].linha_digitavel, '00190.00009 07777.777009 00087.654182 6 49000000295295')

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados[0].barcode, '00196490000002952950000007777777000008765418')


suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoBrasil)
if __name__ == '__main__':
    unittest.main()