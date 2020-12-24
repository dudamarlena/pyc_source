# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybitcointools/bci.py
# Compiled at: 2018-12-04 13:59:45
# Size of source mod 2**32: 17923 bytes
import json, re, random, sys
try:
    from urllib.request import build_opener
except:
    from urllib2 import build_opener

def make_request(*args):
    opener = build_opener()
    opener.addheaders = [
     ('User-agent',
      'Mozilla/5.0' + str(random.randrange(1000000)))]
    try:
        return (opener.open)(*args).read().strip()
    except Exception as e:
        try:
            try:
                p = e.read().strip()
            except:
                p = e

            raise Exception(p)
        finally:
            e = None
            del e


def is_testnet(inp):
    """Checks if inp is a testnet address or if UTXO is a known testnet TxID"""
    if isinstance(inp, (list, tuple)):
        if len(inp) >= 1:
            return any([is_testnet(x) for x in inp])
    if not isinstance(inp, basestring):
        raise TypeError('Input must be str/unicode, not type %s' % str(type(inp)))
    else:
        if not inp or inp.lower() in ('btc', 'testnet'):
            if inp[0] in '123mn':
                if re.match('^[2mn][a-km-zA-HJ-NP-Z0-9]{26,33}$', inp):
                    return True
                    if re.match('^[13][a-km-zA-HJ-NP-Z0-9]{26,33}$', inp):
                        return False
                    return
                else:
                    pass
            if re.match('^[0-9a-fA-F]{64}$', inp):
                base_url = 'http://api.blockcypher.com/v1/btc/{network}/txs/{txid}?includesHex=false'
                try:
                    make_request(base_url.format(network='test3', txid=(inp.lower())))
                    return True
                except:
                    make_request(base_url.format(network='main', txid=(inp.lower())))
                    return False
                    sys.stderr.write('TxID %s has no match for testnet or mainnet (Bad TxID)')
                    return

        raise TypeError('{0} is unknown input'.format(inp))


def set_network(*args):
    """Decides if args for unspent/fetchtx/pushtx are mainnet or testnet"""
    r = []
    for arg in args:
        if not arg:
            if isinstance(arg, basestring):
                r.append(is_testnet(arg))
            elif isinstance(arg, (list, tuple)):
                return set_network(*arg)

    if any(r):
        if not all(r):
            raise Exception('Mixed Testnet/Mainnet queries')
    if any(r):
        return 'testnet'
    return 'btc'


def parse_addr_args(*args):
    addr_args = args
    network = 'btc'
    if len(args) == 0:
        return ([], 'btc')
    if len(args) >= 1:
        if args[(-1)] in ('testnet', 'btc'):
            network = args[(-1)]
            addr_args = args[:-1]
    if len(addr_args) == 1:
        if isinstance(addr_args, list):
            network = set_network(*addr_args[0])
            addr_args = addr_args[0]
    if addr_args:
        if isinstance(addr_args, tuple):
            if isinstance(addr_args[0], list):
                addr_args = addr_args[0]
    network = set_network(addr_args)
    return (network, addr_args)


def bci_unspent(*args):
    network, addrs = parse_addr_args(*args)
    u = []
    for a in addrs:
        try:
            data = make_request('https://blockchain.info/unspent?active=' + a)
        except Exception as e:
            try:
                if str(e) == 'No free outputs to spend':
                    continue
                else:
                    raise Exception(e)
            finally:
                e = None
                del e

        try:
            jsonobj = json.loads(data.decode('utf-8'))
            for o in jsonobj['unspent_outputs']:
                h = o['tx_hash'].decode('hex')[::-1].encode('hex')
                u.append({'output':h + ':' + str(o['tx_output_n']), 
                 'value':o['value']})

        except:
            raise Exception('Failed to decode data: ' + data)

    return u


def blockr_unspent(*args):
    network, addr_args = parse_addr_args(*args)
    if network == 'testnet':
        blockr_url = 'http://tbtc.blockr.io/api/v1/address/unspent/'
    else:
        if network == 'btc':
            blockr_url = 'http://btc.blockr.io/api/v1/address/unspent/'
        else:
            raise Exception('Unsupported network {0} for blockr_unspent'.format(network))
    if len(addr_args) == 0:
        return []
    elif isinstance(addr_args[0], list):
        addrs = addr_args[0]
    else:
        addrs = addr_args
    res = make_request(blockr_url + ','.join(addrs))
    data = json.loads(res.decode('utf-8'))['data']
    o = []
    if 'unspent' in data:
        data = [
         data]
    for dat in data:
        for u in dat['unspent']:
            o.append({'output':u['tx'] + ':' + str(u['n']), 
             'value':int(u['amount'].replace('.', ''))})

    return o


def helloblock_unspent(*args):
    addrs, network = parse_addr_args(*args)
    if network == 'testnet':
        url = 'https://testnet.helloblock.io/v1/addresses/%s/unspents?limit=500&offset=%s'
    else:
        if network == 'btc':
            url = 'https://mainnet.helloblock.io/v1/addresses/%s/unspents?limit=500&offset=%s'
    o = []
    for addr in addrs:
        for offset in xrange(0, 1000000000, 500):
            res = make_request(url % (addr, offset))
            data = json.loads(res.decode('utf-8'))['data']
            if not len(data['unspents']):
                break
            else:
                if offset:
                    sys.stderr.write('Getting more unspents: %d\n' % offset)
            for dat in data['unspents']:
                o.append({'output':dat['txHash'] + ':' + str(dat['index']), 
                 'value':dat['value']})

    return o


unspent_getters = {'bci':bci_unspent, 
 'blockr':blockr_unspent, 
 'helloblock':helloblock_unspent}

def unspent(*args, **kwargs):
    f = unspent_getters.get(kwargs.get('source', ''), bci_unspent)
    return f(*args)


def history(*args):
    if len(args) == 0:
        return []
    elif isinstance(args[0], list):
        addrs = args[0]
    else:
        addrs = args
    txs = []
    for addr in addrs:
        offset = 0
        while True:
            gathered = False
            while not gathered:
                try:
                    data = make_request('https://blockchain.info/address/%s?format=json&offset=%s' % (
                     addr, offset))
                    gathered = True
                except Exception as e:
                    try:
                        try:
                            sys.stderr.write(e.read().strip())
                        except:
                            sys.stderr.write(str(e))

                        gathered = False
                    finally:
                        e = None
                        del e

            try:
                jsonobj = json.loads(data.decode('utf-8'))
            except:
                raise Exception('Failed to decode data: ' + data)

            txs.extend(jsonobj['txs'])
            if len(jsonobj['txs']) < 50:
                break
            offset += 50
            sys.stderr.write('Fetching more transactions... ' + str(offset) + '\n')

    outs = {}
    for tx in txs:
        for o in tx['out']:
            if o.get('addr', None) in addrs:
                key = str(tx['tx_index']) + ':' + str(o['n'])
                outs[key] = {'address':o['addr'], 
                 'value':o['value'], 
                 'output':tx['hash'] + ':' + str(o['n']), 
                 'block_height':tx.get('block_height', None)}

    for tx in txs:
        for i, inp in enumerate(tx['inputs']):
            if 'prev_out' in inp and inp['prev_out'].get('addr', None) in addrs:
                key = str(inp['prev_out']['tx_index']) + ':' + str(inp['prev_out']['n'])
                if outs.get(key):
                    outs[key]['spend'] = tx['hash'] + ':' + str(i)

    return [outs[k] for k in outs]


def bci_pushtx(tx):
    if not re.match('^[0-9a-fA-F]*$', tx):
        tx = tx.encode('hex')
    return make_request('https://blockchain.info/pushtx', 'tx=' + tx)


def eligius_pushtx(tx):
    if not re.match('^[0-9a-fA-F]*$', tx):
        tx = tx.encode('hex')
    s = make_request('http://eligius.st/~wizkid057/newstats/pushtxn.php', 'transaction=' + tx + '&send=Push')
    strings = re.findall('string[^"]*"[^"]*"', s)
    for string in strings:
        quote = re.findall('"[^"]*"', string)[0]
        if len(quote) >= 5:
            return quote[1:-1]


def blockr_pushtx(tx, network='btc'):
    if network == 'testnet':
        blockr_url = 'http://tbtc.blockr.io/api/v1/tx/push'
    else:
        if network == 'btc':
            blockr_url = 'http://btc.blockr.io/api/v1/tx/push'
        else:
            raise Exception('Unsupported network {0} for blockr_pushtx'.format(network))
    if not re.match('^[0-9a-fA-F]*$', tx):
        tx = tx.encode('hex')
    return make_request(blockr_url, '{"hex":"%s"}' % tx)


def helloblock_pushtx(tx):
    if not re.match('^[0-9a-fA-F]*$', tx):
        tx = tx.encode('hex')
    return make_request('https://mainnet.helloblock.io/v1/transactions', 'rawTxHex=' + tx)


pushtx_getters = {'bci':bci_pushtx, 
 'blockr':blockr_pushtx, 
 'helloblock':helloblock_pushtx}

def pushtx(*args, **kwargs):
    f = pushtx_getters.get(kwargs.get('source', ''), bci_pushtx)
    return f(*args)


def last_block_height(network='btc'):
    if network == 'testnet':
        data = make_request('http://tbtc.blockr.io/api/v1/block/info/last')
        jsonobj = json.loads(data.decode('utf-8'))
        return jsonobj['data']['nb']
    data = make_request('https://blockchain.info/latestblock')
    jsonobj = json.loads(data.decode('utf-8'))
    return jsonobj['height']


def bci_fetchtx(txhash):
    if isinstance(txhash, list):
        return [bci_fetchtx(h) for h in txhash]
    if not re.match('^[0-9a-fA-F]*$', txhash):
        txhash = txhash.encode('hex')
    data = make_request('https://blockchain.info/rawtx/' + txhash + '?format=hex')
    return data


def blockr_fetchtx(txhash, network='btc'):
    if network == 'testnet':
        blockr_url = 'http://tbtc.blockr.io/api/v1/tx/raw/'
    else:
        if network == 'btc':
            blockr_url = 'http://btc.blockr.io/api/v1/tx/raw/'
        else:
            raise Exception('Unsupported network {0} for blockr_fetchtx'.format(network))
    if isinstance(txhash, list):
        txhash = ','.join([x.encode('hex') if not re.match('^[0-9a-fA-F]*$', x) else x for x in txhash])
        jsondata = json.loads(make_request(blockr_url + txhash).decode('utf-8'))
        return [d['tx']['hex'] for d in jsondata['data']]
    if not re.match('^[0-9a-fA-F]*$', txhash):
        txhash = txhash.encode('hex')
    jsondata = json.loads(make_request(blockr_url + txhash).decode('utf-8'))
    return jsondata['data']['tx']['hex']


def helloblock_fetchtx(txhash, network='btc'):
    if isinstance(txhash, list):
        return [helloblock_fetchtx(h) for h in txhash]
    elif not re.match('^[0-9a-fA-F]*$', txhash):
        txhash = txhash.encode('hex')
    elif network == 'testnet':
        url = 'https://testnet.helloblock.io/v1/transactions/'
    else:
        if network == 'btc':
            url = 'https://mainnet.helloblock.io/v1/transactions/'
        else:
            raise Exception('Unsupported network {0} for helloblock_fetchtx'.format(network))
    data = json.loads(make_request(url + txhash).decode('utf-8'))['data']['transaction']
    o = {'locktime':data['locktime'], 
     'version':data['version'], 
     'ins':[],  'outs':[]}
    for inp in data['inputs']:
        o['ins'].append({'script':inp['scriptSig'], 
         'outpoint':{'index':inp['prevTxoutIndex'], 
          'hash':inp['prevTxHash']}, 
         'sequence':4294967295})

    for outp in data['outputs']:
        o['outs'].append({'value':outp['value'], 
         'script':outp['scriptPubKey']})

    from pybitcointools.transaction import serialize
    import pybitcointools.transaction as TXHASH
    tx = serialize(o)
    assert TXHASH(tx) == txhash
    return tx


fetchtx_getters = {'bci':bci_fetchtx, 
 'blockr':blockr_fetchtx, 
 'helloblock':helloblock_fetchtx}

def fetchtx(*args, **kwargs):
    f = fetchtx_getters.get(kwargs.get('source', ''), bci_fetchtx)
    return f(*args)


def firstbits(address):
    if len(address) >= 25:
        return make_request('https://blockchain.info/q/getfirstbits/' + address)
    return make_request('https://blockchain.info/q/resolvefirstbits/' + address)


def get_block_at_height(height):
    j = json.loads(make_request('https://blockchain.info/block-height/' + str(height) + '?format=json').decode('utf-8'))
    for b in j['blocks']:
        if b['main_chain'] is True:
            return b

    raise Exception('Block at this height not found')


def _get_block(inp):
    if len(str(inp)) < 64:
        return get_block_at_height(inp)
    return json.loads(make_request('https://blockchain.info/rawblock/' + inp).decode('utf-8'))


def bci_get_block_header_data(inp):
    j = _get_block(inp)
    return {'version':j['ver'], 
     'hash':j['hash'], 
     'prevhash':j['prev_block'], 
     'timestamp':j['time'], 
     'merkle_root':j['mrkl_root'], 
     'bits':j['bits'], 
     'nonce':j['nonce']}


def blockr_get_block_header_data(height, network='btc'):
    if network == 'testnet':
        blockr_url = 'http://tbtc.blockr.io/api/v1/block/raw/'
    else:
        if network == 'btc':
            blockr_url = 'http://btc.blockr.io/api/v1/block/raw/'
        else:
            raise Exception('Unsupported network {0} for blockr_get_block_header_data'.format(network))
    k = json.loads(make_request(blockr_url + str(height)).decode('utf-8'))
    j = k['data']
    return {'version':j['version'], 
     'hash':j['hash'], 
     'prevhash':j['previousblockhash'], 
     'timestamp':j['time'], 
     'merkle_root':j['merkleroot'], 
     'bits':int(j['bits'], 16), 
     'nonce':j['nonce']}


def get_block_timestamp(height, network='btc'):
    if network == 'testnet':
        blockr_url = 'http://tbtc.blockr.io/api/v1/block/info/'
    else:
        if network == 'btc':
            blockr_url = 'http://btc.blockr.io/api/v1/block/info/'
        else:
            raise Exception('Unsupported network {0} for get_block_timestamp'.format(network))
    import time, calendar
    if isinstance(height, list):
        k = json.loads(make_request(blockr_url + ','.join([str(x) for x in height])).decode('utf-8'))
        o = {x['nb']:calendar.timegm(time.strptime(x['time_utc'], '%Y-%m-%dT%H:%M:%SZ')) for x in k['data']}
        return [o[x] for x in height]
    k = json.loads(make_request(blockr_url + str(height)).decode('utf-8'))
    j = k['data']['time_utc']
    return calendar.timegm(time.strptime(j, '%Y-%m-%dT%H:%M:%SZ'))


block_header_data_getters = {'bci':bci_get_block_header_data, 
 'blockr':blockr_get_block_header_data}

def get_block_header_data(inp, **kwargs):
    f = block_header_data_getters.get(kwargs.get('source', ''), bci_get_block_header_data)
    return f(inp, **kwargs)


def get_txs_in_block(inp):
    j = _get_block(inp)
    hashes = [t['hash'] for t in j['tx']]
    return hashes


def get_block_height(txhash):
    j = json.loads(make_request('https://blockchain.info/rawtx/' + txhash).decode('utf-8'))
    return j['block_height']


def get_tx_composite(inputs, outputs, output_value, change_address=None, network=None):
    """mktx using blockcypher API"""
    inputs = [inputs] if not isinstance(inputs, list) else inputs
    outputs = [outputs] if not isinstance(outputs, list) else outputs
    network = set_network(change_address or inputs) if not network else network.lower()
    url = 'http://api.blockcypher.com/v1/btc/{network}/txs/new?includeToSignTx=true'.format(network=('test3' if network == 'testnet' else 'main'))
    is_address = lambda a: bool(re.match('^[123mn][a-km-zA-HJ-NP-Z0-9]{26,33}$', a))
    if any([is_address(x) for x in inputs]):
        inputs_type = 'addresses'
    if any([is_address(x) for x in outputs]):
        outputs_type = 'addresses'
    data = {'inputs':[{inputs_type: inputs}],  'confirmations':0, 
     'preference':'high', 
     'outputs':[
      {outputs_type: outputs, 'value': output_value}]}
    if change_address:
        data['change_address'] = change_address
    jdata = json.loads(make_request(url, data))
    hash, txh = jdata.get('tosign')[0], jdata.get('tosign_tx')[0]
    assert bin_dbl_sha256(txh.decode('hex')).encode('hex') == hash, 'checksum mismatch %s' % hash
    return txh.encode('utf-8')


blockcypher_mktx = get_tx_composite