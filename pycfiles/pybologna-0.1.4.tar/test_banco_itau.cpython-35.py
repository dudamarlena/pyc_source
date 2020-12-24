# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ecereto/src/pyboleto/tests/test_banco_itau.py
# Compiled at: 2016-04-10 23:42:52
# Size of source mod 2**32: 1563 bytes
import unittest, datetime
from pyboleto.bank.itau import BoletoItau
from .testutils import BoletoTestCase

class TestBancoItau(BoletoTestCase):

    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoItau()
            d.carteira = '109'
            d.agencia_cedente = '0293'
            d.conta_cedente = '01328'
            d.data_vencimento = datetime.date(2009, 10, 19)
            d.data_documento = datetime.date(2009, 10, 19)
            d.data_processamento = datetime.date(2009, 10, 19)
            d.valor_documento = 29.8
            d.nosso_numero = str(157 + i)
            d.numero_documento = str(456 + i)
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(self.dados[0].linha_digitavel, '34191.09008 00015.710296 30132.800001 9 43950000002980')

    def test_codigo_de_barras(self):
        self.assertEqual(self.dados[0].barcode, '34199439500000029801090000015710293013280000')

    def test_agencia(self):
        self.assertEqual(self.dados[0].agencia_cedente, '0293')

    def test_conta(self):
        self.assertEqual(self.dados[0].conta_cedente, '01328')

    def test_dv_nosso_numero(self):
        self.assertEqual(self.dados[0].dv_nosso_numero, 1)

    def test_dv_agencia_conta_cedente(self):
        self.assertEqual(self.dados[0].dv_agencia_conta_cedente, 0)


suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoItau)
if __name__ == '__main__':
    unittest.main()