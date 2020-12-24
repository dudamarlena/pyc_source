# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\trans\protobuf_test.py
# Compiled at: 2020-04-22 08:41:02
# Size of source mod 2**32: 1497 bytes
import unittest, base64
from bsn_sdk_py.trans.transaction_header import created_peer_chaincode_chaincodeinvocationspec, created_peer_chaincode_chaincodeinput, created_peer_chaincode_chaincodespec, created_peer_chaincode_chaincodeid

class TestRequest(unittest.TestCase):

    def test_ChaincodeInvocationSpec(self):
        args_bytes = [
         '111']
        chaincodeId = 'app0006202004071529586812466'
        funcName = 'set'
        args = []
        args.append(bytes(funcName, 'utf-8'))
        for a in args_bytes:
            args.append(bytes(a, 'utf-8'))

        peer_chaincode_chaincodeinput = created_peer_chaincode_chaincodeinput(args)
        print('chaincodeInput_s:', base64.b64encode(peer_chaincode_chaincodeinput.SerializeToString()))
        chaincodeId_obj = created_peer_chaincode_chaincodeid(chaincodeId)
        print('chaincodeID_s:', base64.b64encode(chaincodeId_obj.SerializeToString()))
        peer_chaincode_chaincodespec = created_peer_chaincode_chaincodespec(chaincodeId_obj, peer_chaincode_chaincodeinput)
        print('chaincodeSpec_s:', base64.b64encode(peer_chaincode_chaincodespec.SerializeToString()))
        peer_chaincode_chaincodeinvocationspec = created_peer_chaincode_chaincodeinvocationspec(peer_chaincode_chaincodespec)
        spec = peer_chaincode_chaincodeinvocationspec.SerializeToString()
        print('ccis:', base64.b64encode(spec))