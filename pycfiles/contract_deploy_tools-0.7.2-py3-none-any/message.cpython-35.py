# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/chain/message.py
# Compiled at: 2015-12-14 09:35:21
# Size of source mod 2**32: 3640 bytes
import random, json, logging, binascii, hashlib
from pycoin.tx.Tx import *
from pycoin.tx.script import tools
from pycoin import encoding
from pycoin.networks import *
from pycoin.serialize import b2h, b2h_rev, h2b, h2b_rev
from .. import config
from ..proto import Protocol
logger = logging.getLogger(config.APP_NAME)

class Message:

    def __init__(self):
        self.Transaction = None
        self.Method = None
        self.DappCode = None
        self.Protocol = Protocol.VERSION
        self.Data = None
        self.Hash = ''
        self.Player = ''
        self.Block = 0
        self.DataHash = None

    def toJSON(self):
        data = {'method': self.Method, 'player': self.Player}
        return data

    def getDataHash(self, data):
        return hashlib.sha256(data.encode('ascii')).hexdigest().encode('ascii')

    def toOutputScript(self, dht):
        jdata = self.toJSON()
        data = json.dumps(self.toJSON(), (':', ','))
        if data == None:
            assert 'Data is none'
        datahash = self.getDataHash(data)
        temp_id = dht.prepare(data)
        opret = Protocol.MAGIC_FLAG + chr(self.Protocol) + chr(self.DappCode[0]) + chr(self.DappCode[1]) + chr(self.Method) + datahash.decode()
        retscript = 'OP_RETURN ' + str(binascii.hexlify(opret.encode('ascii')))[2:-1]
        if len(retscript) > Protocol.STORAGE_OPRETURN_LIMIT:
            assert 'Transaction data is too big'
        return [
         datahash.decode(), retscript, temp_id]

    def isMessage(txhex):
        tx = Tx.from_hex(txhex)
        oprets = []
        for txout in tx.txs_out:
            ops = tools.opcode_list(txout.script)
            if len(ops) > 0 and ops[0] == 'OP_RETURN':
                oprets.append(ops[1])

        if len(oprets) == 0:
            return False
        for opret in oprets:
            data = ''.join(chr(int(opret[i:i + 2], 16)) for i in range(0, len(opret), 2))
            if data[0:len(Protocol.MAGIC_FLAG)] != Protocol.MAGIC_FLAG:
                continue
            else:
                return True

        return False

    def fromTransaction(blockn, txhex):
        tx = Tx.from_hex(txhex)
        oprets = []
        for txout in tx.txs_out:
            ops = tools.opcode_list(txout.script)
            if len(ops) > 0 and ops[0] == 'OP_RETURN':
                oprets.append(ops[1])

        if len(oprets) == 0:
            return
        for opret in oprets:
            try:
                data = ''.join(chr(int(opret[i:i + 2], 16)) for i in range(0, len(opret), 2))
            except:
                continue

            if data[0:len(Protocol.MAGIC_FLAG)] != Protocol.MAGIC_FLAG:
                pass
            continue
            m = Message()
            m.Protocol = ord(data[len(Protocol.MAGIC_FLAG):len(Protocol.MAGIC_FLAG) + 1])
            m.DappCode = [ord(data[len(Protocol.MAGIC_FLAG) + 1:len(Protocol.MAGIC_FLAG) + 2]), ord(data[len(Protocol.MAGIC_FLAG) + 2:len(Protocol.MAGIC_FLAG) + 3])]
            m.Method = ord(data[len(Protocol.MAGIC_FLAG) + 3:len(Protocol.MAGIC_FLAG) + 4])
            m.Hash = tx.id()
            m.Block = blockn
            m.DataHash = data[len(Protocol.MAGIC_FLAG) + 4:len(Protocol.MAGIC_FLAG) + 4 + Protocol.DATA_HASH_SIZE].encode('ascii')
            m.Player = tx.txs_in[0].bitcoin_address(address_prefix_for_netcode(config.CONF['chain']))
            return m