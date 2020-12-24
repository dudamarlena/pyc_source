# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\test\register_user.py
# Compiled at: 2020-04-23 03:42:41
# Size of source mod 2**32: 4949 bytes
import unittest
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.fabric_client import FabricClient
import logging
c = Config(user_code='USER0001202004151958010871292', app_code='app0001202004161020152918451', nodeApi='http://192.168.1.43:17502',
  mspDir='E:\\hz_workspace\\study\\bsn_sdk_py\\test',
  httpcert='',
  user_private_cert_path='E:\\hz_workspace\\study\\bsn_sdk_py\\test\\private.pem',
  app_public_cert_path='E:\\hz_workspace\\study\\bsn_sdk_py\\test\\public.pem')

class TestBsn(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('这是所有case的前置条件01')

    @classmethod
    def tearDownClass(cls):
        print('这是所有case的后置条件01')

    def setUp(self):
        print('这是每条case的前置条件01')
        FORMAT = '%(asctime)s %(thread)d %(message)s'
        logging.basicConfig(filename='bsn_test.log', filemode='w', level=(logging.INFO), format=FORMAT, datefmt='[%Y-%m-%d %H:%M:%S]')
        client = FabricClient()
        client.set_config(c)
        self.client = client

    def tearDown(self):
        print('这是每条case的后置条件01')

    def test_req_chain_code(self):
        print('Test: 密钥托管模式交易处理')
        self.client.req_chain_code(chainCode='cc_app0001202004161017141233920_00', funcName='set', name='', args=[
         '{"baseKey":"test20200415","baseValue":"this is string "}'],
          transientData={})

    def test_get_transaction(self):
        print('Test:获取交易信息')
        txId = '3cab3a400ac14de911a3fd4ac08dd4d5d7993e18a97ab2c389313d3082afd427'
        self.client.get_transaction(txId)

    @unittest.skip('不执行这条case')
    def test_skip(self):
        print('01: 第二条case')

    def test_get_block_info(self):
        print('Test:获取块信息')
        txId = '364a7ce7c1f7c3fb7afb3ea2b9c678ed3dfd5e7c61ae72c4541822646fd24a19'
        self.client.get_block_info(txId=txId)

    def test_get_ledger_info(self):
        print('Test:获取最新账本信息')
        self.client.get_ledger_info()

    def test_event_register(self):
        print('Test:链码事件注册')
        chainCode = 'cc_app0001202004161020152918451_00'
        eventKey = 'test'
        notifyUrl = 'http://127.0.0.1'
        attachArgs = 'a=1'
        self.client.event_register(chainCode, eventKey, notifyUrl, attachArgs)

    def test_event_query(self):
        print('Test:链码事件查询')
        self.client.event_query()

    def test_event_remove(self):
        print('Test:链码事件查询')
        eventId = 'c70f0bc10a444bc4a1d916b05ffc6064'
        self.client.event_remove(eventId)

    def test_register_user(self):
        print('Test:用户注册')
        eventId = 'c70f0bc10a444bc4a1d916b05ffc6064'
        self.client.register_user('hll4', '123456')

    def test_enroll_user(self):
        print('Test:密钥非托管模式用户证书登记')
        eventId = 'c70f0bc10a444bc4a1d916b05ffc6064'
        self.client.enroll_user('hll4', '123456')

    def test_notrust_trans(self):
        print('Test:密钥非托管模式用户证书登记')
        self.client.not_trust_trans(chainCode='cc_app0001202004161020152918451_00', funcName='set', name='hll4', args=[
         '{"baseKey":"111","baseValue":"this is string "}'],
          transientData={})


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestBsn('test_get_transaction'))
    unittest.TextTestRunner().run(suite)