# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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