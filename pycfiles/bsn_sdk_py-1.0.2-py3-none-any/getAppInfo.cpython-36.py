# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\test\getAppInfo.py
# Compiled at: 2020-04-20 03:17:26
# Size of source mod 2**32: 909 bytes
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.fabric_client import FabricClient
c = Config(user_code='USER0001202004151958010871292', app_code='app0001202004161020152918451', nodeApi='http://192.168.1.43:17502',
  mspDir='E:\\hz_workspace\\study\\bsn_sdk_py\\test',
  httpcert='',
  user_private_cert_path='E:\\hz_workspace\\study\\bsn_sdk_py\\test\\private.pem',
  app_public_cert_path='E:\\hz_workspace\\study\\bsn_sdk_py\\test\\public.pem')
client = FabricClient()
client.set_config(c)
client.req_chain_code(chainCode='cc_app0001202004161020152918451_00', funcName='set', name='', args=[
 '{"baseKey":"test20200415","baseValue":"this is string "}'],
  transientData={})