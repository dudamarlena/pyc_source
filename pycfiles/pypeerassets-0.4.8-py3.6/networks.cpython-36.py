# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypeerassets/networks.py
# Compiled at: 2018-08-27 16:42:20
# Size of source mod 2**32: 2498 bytes
from collections import namedtuple
from decimal import Decimal
from btcpy.structs.transaction import TxOut
from btcpy.structs.script import NulldataScript
from pypeerassets.exceptions import UnsupportedNetwork

class PeercoinTxOut(TxOut):

    def get_dust_threshold(self, size_to_relay_fee) -> float:
        if isinstance(self.script_pubkey, NulldataScript):
            return 0
        else:
            return 0.01


Constants = namedtuple('Constants', [
 'name',
 'shortname',
 'base58_prefixes',
 'base58_raw_prefixes',
 'bech32_hrp',
 'bech32_net',
 'xkeys_prefix',
 'xpub_version',
 'xprv_version',
 'wif_prefix',
 'from_unit',
 'to_unit',
 'min_tx_fee',
 'tx_timestamp',
 'tx_out_cls',
 'op_return_max_bytes'])
PeercoinMainnet = Constants(name='peercoin',
  shortname='ppc',
  base58_prefixes={'P':'p2pkh', 
 'p':'p2sh'},
  base58_raw_prefixes={'p2pkh':bytearray(b'7'), 
 'p2sh':bytearray(b'u')},
  bech32_hrp='bc',
  bech32_net='mainnet',
  xkeys_prefix='x',
  xpub_version=b'\x04\x88\xb2\x1e',
  xprv_version=b'\x04\x88\xad\xe4',
  wif_prefix=183,
  from_unit=(Decimal('1e-6')),
  to_unit=(Decimal('1e6')),
  min_tx_fee=(Decimal(0.01)),
  tx_timestamp=True,
  tx_out_cls=PeercoinTxOut,
  op_return_max_bytes=80)
PeercoinTestnet = Constants(name='peercoin-testnet',
  shortname='tppc',
  base58_prefixes={'m':'p2pkh', 
 'n':'p2pkh'},
  base58_raw_prefixes={'p2pkh':bytearray(b'o'), 
 'p2sh':bytearray(b'\xc4')},
  bech32_hrp='tb',
  bech32_net='testnet',
  xkeys_prefix='t',
  xpub_version=b'\x045\x87\xcf',
  xprv_version=b'\x045\x83\x94',
  wif_prefix=239,
  from_unit=(Decimal('1e-6')),
  to_unit=(Decimal('1e6')),
  min_tx_fee=(Decimal(0.01)),
  tx_timestamp=True,
  tx_out_cls=PeercoinTxOut,
  op_return_max_bytes=80)
networks = (
 PeercoinMainnet, PeercoinTestnet)

def net_query(name: str) -> Constants:
    """Find the NetworkParams for a network by its long or short name. Raises
    UnsupportedNetwork if no NetworkParams is found.
    """
    for net_params in networks:
        if name in (net_params.name, net_params.shortname):
            return net_params

    raise UnsupportedNetwork