# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/blockcypher/constants.py
# Compiled at: 2020-01-07 12:17:40
COIN_SYMBOL_ODICT_LIST = [
 {'coin_symbol': 'btc', 
    'display_name': 'Bitcoin', 
    'display_shortname': 'BTC', 
    'blockcypher_code': 'btc', 
    'blockcypher_network': 'main', 
    'currency_abbrev': 'BTC', 
    'pow': 'sha', 
    'example_address': '16Fg2yjwrbtC6fZp61EV9mNVKmwCzGasw5', 
    'address_first_char_list': ('1', '3', '4', 'b'), 
    'singlesig_prefix_list': ('1', 'b'), 
    'multisig_prefix_list': ('3', ), 
    'bech32_prefix': 'bc1', 
    'first4_mprv': 'xprv', 
    'first4_mpub': 'xpub', 
    'vbyte_pubkey': 0, 
    'vbyte_script': 5},
 {'coin_symbol': 'btc-testnet', 
    'display_name': 'Bitcoin Testnet', 
    'display_shortname': 'BTC Testnet', 
    'blockcypher_code': 'btc', 
    'blockcypher_network': 'test3', 
    'currency_abbrev': 'BTC', 
    'pow': 'sha', 
    'example_address': '2N1rjhumXA3ephUQTDMfGhufxGQPZuZUTMk', 
    'address_first_char_list': ('m', 'n', '2', 'z', 't'), 
    'singlesig_prefix_list': ('m', 'n', 't'), 
    'multisig_prefix_list': ('2', ), 
    'bech32_prefix': 'tb1', 
    'first4_mprv': 'tprv', 
    'first4_mpub': 'tpub', 
    'vbyte_pubkey': 111, 
    'vbyte_script': 196},
 {'coin_symbol': 'ltc', 
    'display_name': 'Litecoin', 
    'display_shortname': 'LTC', 
    'blockcypher_code': 'ltc', 
    'blockcypher_network': 'main', 
    'currency_abbrev': 'LTC', 
    'pow': 'scrypt', 
    'example_address': 'LcFFkbRUrr8j7TMi8oXUnfR4GPsgcXDepo', 
    'address_first_char_list': ('L', 'U', 'M', '3', '4'), 
    'singlesig_prefix_list': ('L', ), 
    'multisig_prefix_list': ('3', 'M'), 
    'bech32_prefix': 'ltc1', 
    'first4_mprv': 'Ltpv', 
    'first4_mpub': 'Ltub', 
    'vbyte_pubkey': 48, 
    'vbyte_script': 5},
 {'coin_symbol': 'doge', 
    'display_name': 'Dogecoin', 
    'display_shortname': 'DOGE', 
    'blockcypher_code': 'doge', 
    'blockcypher_network': 'main', 
    'currency_abbrev': 'DOGE', 
    'pow': 'scrypt', 
    'example_address': 'D7Y55r6Yoc1G8EECxkQ6SuSjTgGJJ7M6yD', 
    'address_first_char_list': ('D', '9', 'A', '2'), 
    'singlesig_prefix_list': ('D', ), 
    'multisig_prefix_list': ('9', 'A'), 
    'bech32_prefix': 'xyz', 
    'first4_mprv': 'dgpv', 
    'first4_mpub': 'dgub', 
    'vbyte_pubkey': 30, 
    'vbyte_script': 22},
 {'coin_symbol': 'dash', 
    'display_name': 'Dash', 
    'display_shortname': 'DASH', 
    'blockcypher_code': 'dash', 
    'blockcypher_network': 'main', 
    'currency_abbrev': 'DASH', 
    'pow': 'scrypt', 
    'example_address': 'XdZW5Waa1i6D9za3qpFvgiwHzr8aFcXtNP', 
    'address_first_char_list': 'X', 
    'singlesig_prefix_list': ('X', ), 
    'multisig_prefix_list': ('7', ), 
    'bech32_prefix': 'xyz', 
    'first4_mprv': 'xprv', 
    'first4_mpub': 'xpub', 
    'vbyte_pubkey': 76, 
    'vbyte_script': 16},
 {'coin_symbol': 'bcy', 
    'display_name': 'BlockCypher Testnet', 
    'display_shortname': 'BCY Testnet', 
    'blockcypher_code': 'bcy', 
    'blockcypher_network': 'test', 
    'currency_abbrev': 'BCY', 
    'pow': 'sha', 
    'example_address': 'CFr99841LyMkyX5ZTGepY58rjXJhyNGXHf', 
    'address_first_char_list': ('B', 'C', 'D', 'Y', 'b'), 
    'singlesig_prefix_list': ('C', 'B'), 
    'multisig_prefix_list': ('D', ), 
    'bech32_prefix': 'bcy1', 
    'first4_mprv': 'bprv', 
    'first4_mpub': 'bpub', 
    'vbyte_pubkey': 27, 
    'vbyte_script': 31}]
REQUIRED_FIELDS = ('coin_symbol', 'display_name', 'display_shortname', 'blockcypher_code',
                   'blockcypher_network', 'currency_abbrev', 'pow', 'example_address',
                   'address_first_char_list', 'singlesig_prefix_list', 'multisig_prefix_list',
                   'first4_mprv', 'first4_mpub', 'vbyte_pubkey', 'vbyte_script')
ELIGIBLE_POW_ENTRIES = set(['sha', 'scrypt', 'x11'])
for coin_symbol_dict in COIN_SYMBOL_ODICT_LIST:
    assert coin_symbol_dict['pow'] in ELIGIBLE_POW_ENTRIES, coin_symbol_dict['pow']
    for required_field in REQUIRED_FIELDS:
        assert required_field in coin_symbol_dict

COIN_SYMBOL_LIST = [ x['coin_symbol'] for x in COIN_SYMBOL_ODICT_LIST ]
COIN_SYMBOL_SET = set(COIN_SYMBOL_LIST)
SHA_COINS = [ x['coin_symbol'] for x in COIN_SYMBOL_ODICT_LIST if x['pow'] == 'sha' ]
SCRYPT_COINS = [ x['coin_symbol'] for x in COIN_SYMBOL_ODICT_LIST if x['pow'] == 'scrypt' ]
COIN_CHOICES = []
for coin_symbol_dict in COIN_SYMBOL_ODICT_LIST:
    COIN_CHOICES.append((coin_symbol_dict['coin_symbol'], coin_symbol_dict['display_name']))

FIRST4_MKEY_CS_MAPPINGS_UPPER = {}
for coin_symbol_dict in COIN_SYMBOL_ODICT_LIST:
    if 'first4_mprv' in coin_symbol_dict:
        FIRST4_MKEY_CS_MAPPINGS_UPPER[coin_symbol_dict['first4_mprv'].upper()] = coin_symbol_dict['coin_symbol']
    if 'first4_mpub' in coin_symbol_dict:
        FIRST4_MKEY_CS_MAPPINGS_UPPER[coin_symbol_dict['first4_mpub'].upper()] = coin_symbol_dict['coin_symbol']

COIN_SYMBOL_MAPPINGS = {}
for coin_symbol_dict in COIN_SYMBOL_ODICT_LIST:
    coin_symbol = coin_symbol_dict.pop('coin_symbol')
    COIN_SYMBOL_MAPPINGS[coin_symbol] = coin_symbol_dict

UNIT_CHOICE_ODICT_LIST = [
 {'unit': 'btc', 
    'display_name': 'BTC', 
    'satoshis_per': 100000000},
 {'unit': 'mbtc', 
    'display_name': 'mBTC', 
    'satoshis_per': 100000},
 {'unit': 'bit', 
    'display_name': 'bit', 
    'satoshis_per': 100},
 {'display_name': 'satoshi', 
    'unit': 'satoshi'}]
UNIT_CHOICES = []
UNIT_CHOICES_DJANGO = []
for unit_choice_dict in UNIT_CHOICE_ODICT_LIST:
    UNIT_CHOICES.append(unit_choice_dict['unit'])
    UNIT_CHOICES_DJANGO.append((unit_choice_dict['unit'], unit_choice_dict['display_name']))

UNIT_MAPPINGS = {}
for unit_choice_dict in UNIT_CHOICE_ODICT_LIST:
    unit_choice = unit_choice_dict.pop('unit')
    UNIT_MAPPINGS[unit_choice] = unit_choice_dict