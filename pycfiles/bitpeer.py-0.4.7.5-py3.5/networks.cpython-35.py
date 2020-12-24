# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitpeer/networks.py
# Compiled at: 2015-11-28 06:41:36
# Size of source mod 2**32: 2089 bytes
SUPPORTED_CHAINS = [
 'BTC', 'XTN', 'NMC', 'LTC', 'XLT', 'DOGE', 'XDN']
MAGIC_VALUES = {'BTC': 3652501241, 
 'XTN': 118034699, 
 'NMC': 4273258233, 
 'LTC': 4223710939, 
 'XLT': 3703030268, 
 'DOGE': 3233857728, 
 'XDN': 3703030268}
GENESIS = {'BTC': 10628944869218562084050143519444549580389464591454674019345556079, 
 'XTN': 969166842145694355898879064562217049827305169495536240246191507779, 
 'NMC': 40609209818120982686391914537603547724473954170922252773255399280, 
 'LTC': 8437397933974567076152334220308321147591132710429995271181962861107589988322, 
 'XLT': 111124865293878591669737467409687674426692482516671004227053451149550966863503, 
 'DOGE': 12017899482963797479678859651879910581716609165137857801054999581379236550289, 
 'XDN': 84601000397152776311069875044200555746694937165252838514302038040702912320926}
PORTS = {'BTC': 8333, 
 'XTN': 18333, 
 'NMC': 8334, 
 'LTC': 9333, 
 'XLT': 19333, 
 'DOGE': 22556, 
 'XDN': 44556}
PEERS = {'BTC': [('bitcoin.sipa.be', 8333)], 
 'XTN': [], 
 'NMC': [], 
 'LTC': [], 
 'XLT': [('51.254.215.160', 19333)]}
SEEDS = {'BTC': ['seed.bitcoin.sipa.be', 'dnsseed.bluematt.me', 'dnsseed.bitcoin.dashjr.org', 'seed.bitcoinstats.com', 'bitseed.xf2.org'], 
 'XTN': ['testnet-seed.alexykot.me', 'testnet-seed.bitcoin.petertodd.org', 'testnet-seed.bluematt.me', 'testnet-seed.bitcoin.schildbach.de'], 
 'LTC': ['dnsseed.litecointools.com', 'dnsseed.litecoinpool.org', 'dnsseed.ltc.xurious.com', 'dnsseed.koin-project.com', 'dnsseed.weminemnc.com'], 
 'XLT': ['testnet-seed.litecointools.com', 'testnet-seed.ltc.xurious.com', 'dnsseed.wemine-testnet.com'], 
 'NMC': ['namecoindnsseed.digi-masters.com', 'namecoindnsseed.digi-masters.uk', 'seed.namecoin.domob.eu', 'nmc.seed.quisquis.de', 'dnsseed.namecoin.webbtc.com'], 
 'DOGE': ['seed.dogecoin.com', 'seed.multidoge.org', 'seed2.multidoge.org', 'seed.doger.dogecoin.com'], 
 'XDN': ['testseed.jrn.me.uk']}

class UnsupportedChainException(Exception):
    pass


def isSupported(chain):
    return chain.upper() in SUPPORTED_CHAINS