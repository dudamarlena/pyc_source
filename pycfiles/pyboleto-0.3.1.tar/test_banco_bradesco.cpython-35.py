# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ecereto/src/pyboleto/tests/test_banco_bradesco.py
# Compiled at: 2016-04-10 23:42:52
# Size of source mod 2**32: 1389 bytes
import unittest, datetime
from pyboleto.bank.bradesco import BoletoBradesco
from .testutils import BoletoTestCase

class TestBancoBradesco(BoletoTestCase):

    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoBradesco()
            d.carteira = '06'
            d.agencia_cedente = '278-0'
            d.conta_cedente = '039232-4'
            d.data_vencimento = datetime.date(2011, 2, 5)
            d.data_documento = datetime.date(2011, 1, 18)
            d.data_processamento = datetime.date(2011, 1, 18)
            d.valor_documento = 8280.0
            d.nosso_numero = str(2125525 + i)
            d.numero_documento = str(2125525 + i)
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(self.dados[0].linha_digitavel, '23790.27804 60000.212559 25003.923205 4 48690000828000')

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados[0].barcode, '23794486900008280000278060000212552500392320')

    def test_agencia(self):
        self.assertEqual(self.dados[0].agencia_cedente, '0278-0')

    def test_conta(self):
        self.assertEqual(self.dados[0].conta_cedente, '0039232-4')


suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoBradesco)
if __name__ == '__main__':
    unittest.main()