# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/names.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 10648 bytes


def split_name_script(decoded):
    if decoded is None:
        return {'name_op':None, 
         'address_scriptPubKey':decoded}
    match = [
     OP_NAME_REGISTER, OPPushDataGeneric, OPPushDataGeneric, opcodes.OP_2DROP, opcodes.OP_DROP]
    if match_decoded(decoded[:len(match)], match):
        return {'name_op':{'op':OP_NAME_REGISTER, 
          'name':decoded[1][1],  'value':decoded[2][1]}, 
         'address_scriptPubKey':decoded[len(match):]}
    match = [
     OP_NAME_UPDATE, OPPushDataGeneric, OPPushDataGeneric, opcodes.OP_2DROP, opcodes.OP_DROP]
    if match_decoded(decoded[:len(match)], match):
        return {'name_op':{'op':OP_NAME_UPDATE, 
          'name':decoded[1][1],  'value':decoded[2][1]}, 
         'address_scriptPubKey':decoded[len(match):]}
    return {'name_op':None,  'address_scriptPubKey':decoded}


def get_name_op_from_output_script(_bytes):
    try:
        decoded = [x for x in script_GetOp(_bytes)]
    except MalformedBitcoinScript:
        decoded = None

    return split_name_script(decoded)['name_op']


def name_op_to_script(name_op):
    if name_op is None:
        script = ''
    else:
        if name_op['op'] == OP_NAME_REGISTER:
            validate_update_length(name_op)
            script = '51'
            script += push_script(bh2u(name_op['name']))
            script += push_script(bh2u(name_op['value']))
            script += '6d'
            script += '75'
        else:
            if name_op['op'] == OP_NAME_UPDATE:
                validate_update_length(name_op)
                script = '52'
                script += push_script(bh2u(name_op['name']))
                script += push_script(bh2u(name_op['value']))
                script += '6d'
                script += '75'
            else:
                raise BitcoinException('unknown name op: {}'.format(name_op))
    return script


def validate_update_length(name_op):
    validate_anyupdate_length(name_op)


def validate_anyupdate_length(name_op):
    validate_identifier_length(name_op['name'])
    validate_value_length(name_op['value'])


def validate_identifier_length(identifier):
    identifier_length_limit = 256
    identifier_length = len(identifier)
    if identifier_length > identifier_length_limit:
        raise BitcoinException('identifier length {} exceeds limit of {}'.format(identifier_length, identifier_length_limit))


def validate_value_length(value):
    if len(value) == 0:
        return
        value_length_limit = 2048
        value_length = len(value)
        if value_length > value_length_limit:
            raise BitcoinException('value length {} exceeds limit of {}'.format(value_length, value_length_limit))
    else:
        import json
        try:
            parsed = json.loads(value)
            if not isinstance(parsed, dict):
                raise BitcoinException(f"Value is not a JSON object: {value}")
        except json.decoder.JSONDecodeError:
            raise BitcoinException(f"Value is invalid JSON: {value}")


def name_identifier_to_scripthash(identifier_bytes):
    name_op = {'op':OP_NAME_UPDATE, 
     'name':identifier_bytes,  'value':bytes([])}
    script = name_op_to_script(name_op)
    script += '6a'
    return script_to_scripthash(script)


def format_name_identifier(identifier_bytes):
    try:
        identifier = identifier_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return format_name_identifier_unknown_hex(identifier_bytes)
    else:
        if identifier.startswith('p/'):
            return format_name_identifier_player(identifier)
        if identifier.startswith('g/'):
            return format_name_identifier_game(identifier)
        return format_name_identifier_unknown(identifier)


def format_name_identifier_player(identifier):
    label = identifier[len('p/'):]
    return f"Player: {label}"


def format_name_identifier_game(identifier):
    label = identifier[len('g/'):]
    return f"Game: {label}"


def format_name_identifier_unknown(identifier):
    if identifier.isprintable():
        return 'Non-standard name "' + identifier + '"'
    return format_name_identifier_unknown_hex(identifier.encode('ascii'))


def format_name_identifier_unknown_hex(identifier_bytes):
    return 'Non-standard hex name ' + bh2u(identifier_bytes)


def format_name_value(identifier_bytes):
    try:
        identifier = identifier_bytes.decode('ascii')
    except UnicodeDecodeError:
        return format_name_value_hex(identifier_bytes)
    else:
        if not identifier.isprintable():
            return format_name_value_hex(identifier_bytes)
        return 'JSON ' + identifier


def format_name_value_hex(identifier_bytes):
    return 'Hex ' + bh2u(identifier_bytes)


def format_name_op(name_op):
    if name_op is None:
        return ''
    if 'name' in name_op:
        formatted_name = 'Name = ' + format_name_identifier(name_op['name'])
    if 'value' in name_op:
        formatted_value = 'Data = ' + format_name_value(name_op['value'])
    if name_op['op'] == OP_NAME_REGISTER:
        return '\tRegistration\n\t\t' + formatted_name + '\n\t\t' + formatted_value
    if name_op['op'] == OP_NAME_UPDATE:
        return '\tUpdate\n\t\t' + formatted_name + '\n\t\t' + formatted_value


def get_default_name_tx_label(wallet, tx):
    for idx, o in enumerate(tx.outputs()):
        name_op = o.name_op
        if name_op is not None:
            name_input_is_mine, name_output_is_mine, name_value_is_unchanged = get_wallet_name_delta(wallet, tx)
        if not name_input_is_mine:
            if not name_output_is_mine:
                return
            else:
                if name_op['op'] == OP_NAME_REGISTER:
                    return 'Registration: ' + format_name_identifier(name_op['name'])
                if name_input_is_mine:
                    return name_output_is_mine or 'Transfer (Outgoing): ' + format_name_identifier(name_op['name'])
            if not name_input_is_mine:
                if name_output_is_mine:
                    return 'Transfer (Incoming): ' + format_name_identifier(name_op['name'])
            if name_op['op'] == OP_NAME_UPDATE:
                return 'Update: ' + format_name_identifier(name_op['name'])


def get_wallet_name_delta(wallet, tx):
    name_input_is_mine = False
    name_output_is_mine = False
    name_input_value = None
    name_output_value = None
    for txin in tx.inputs():
        addr = wallet.get_txin_address(txin)
        if wallet.is_mine(addr):
            prev_tx = wallet.db.transactions.get(txin['prevout_hash'])
            if prev_tx.outputs()[txin['prevout_n']].name_op is not None:
                name_input_is_mine = True
                if 'value' in prev_tx.outputs()[txin['prevout_n']].name_op:
                    name_input_value = prev_tx.outputs()[txin['prevout_n']].name_op['value']

    for o in tx.outputs():
        if o.name_op is not None and wallet.is_mine(o.address):
            name_output_is_mine = True
            if 'value' in o.name_op:
                name_output_value = o.name_op['value']

    name_value_is_unchanged = name_input_value == name_output_value
    return (
     name_input_is_mine, name_output_is_mine, name_value_is_unchanged)


def get_wallet_name_count(wallet, network):
    confirmed_count = 0
    pending_count = 0
    utxos = wallet.get_utxos()
    for _, x in enumerate(utxos):
        txid = x.get('prevout_hash')
        vout = x.get('prevout_n')
        name_op = wallet.db.transactions[txid].outputs()[vout].name_op
        if name_op is None:
            continue
        height = x.get('height')
        if height <= 0:
            if name_op['op'] == OP_NAME_REGISTER:
                pending_count += 1
                continue
            else:
                confirmed_count += 1
                continue
        if 'name' in name_op:
            confirmed_count += 1
            continue
        else:
            pending_count += 1
            continue

    return (
     confirmed_count, pending_count)


import binascii
from datetime import datetime, timedelta
import os, re
from .bitcoin import push_script, script_to_scripthash
from .crypto import hash_160
from .transaction import MalformedBitcoinScript, match_decoded, opcodes, OPPushDataGeneric, script_GetOp, Transaction
from .util import bh2u, BitcoinException
OP_NAME_REGISTER = opcodes.OP_1
OP_NAME_UPDATE = opcodes.OP_2