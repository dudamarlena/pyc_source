# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socketio/packet.py
# Compiled at: 2014-02-03 00:13:04
from socketio.defaultjson import default_json_dumps, default_json_loads
MSG_TYPES = {'disconnect': 0, 
   'connect': 1, 
   'heartbeat': 2, 
   'message': 3, 
   'json': 4, 
   'event': 5, 
   'ack': 6, 
   'error': 7, 
   'noop': 8}
MSG_VALUES = dict((v, k) for (k, v) in MSG_TYPES.iteritems())
ERROR_REASONS = {'transport not supported': 0, 
   'client not handshaken': 1, 
   'unauthorized': 2}
REASONS_VALUES = dict((v, k) for (k, v) in ERROR_REASONS.iteritems())
ERROR_ADVICES = {'reconnect': 0}
ADVICES_VALUES = dict((v, k) for (k, v) in ERROR_ADVICES.iteritems())
socketio_packet_attributes = [
 'type', 'name', 'data', 'endpoint', 'args',
 'ackId', 'reason', 'advice', 'qs', 'id']

def encode(data, json_dumps=default_json_dumps):
    """
    Encode an attribute dict into a byte string.
    """
    payload = ''
    msg = str(MSG_TYPES[data['type']])
    if msg in ('0', '1'):
        msg += '::' + data['endpoint']
        if 'qs' in data and data['qs'] != '':
            msg += ':' + data['qs']
    elif msg == '2':
        msg += '::'
    elif msg in ('3', '4', '5'):
        if msg == '3':
            payload = data['data']
        if msg == '4':
            payload = json_dumps(data['data'])
        if msg == '5':
            d = {}
            d['name'] = data['name']
            if 'args' in data and data['args'] != []:
                d['args'] = data['args']
            payload = json_dumps(d)
        if 'id' in data:
            msg += ':' + str(data['id'])
            if data['ack'] == 'data':
                msg += '+'
            msg += ':'
        else:
            msg += '::'
        if 'endpoint' not in data:
            data['endpoint'] = ''
        if payload != '':
            msg += data['endpoint'] + ':' + payload
        else:
            msg += data['endpoint']
    elif msg == '6':
        msg += '::' + data.get('endpoint', '') + ':' + str(data['ackId'])
        if 'args' in data and data['args'] != []:
            msg += '+' + json_dumps(data['args'])
    elif msg == '7':
        msg += ':::'
        if 'reason' in data and data['reason'] != '':
            msg += str(ERROR_REASONS[data['reason']])
        if 'advice' in data and data['advice'] != '':
            msg += '+' + str(ERROR_ADVICES[data['advice']])
        msg += data['endpoint']
    elif msg == '8':
        msg += '::'
    return msg


def decode(rawstr, json_loads=default_json_loads):
    """
    Decode a rawstr packet arriving from the socket into a dict.
    """
    decoded_msg = {}
    split_data = rawstr.split(':', 3)
    msg_type = split_data[0]
    msg_id = split_data[1]
    endpoint = split_data[2]
    data = ''
    if msg_id != '':
        if '+' in msg_id:
            msg_id = msg_id.split('+')[0]
            decoded_msg['id'] = int(msg_id)
            decoded_msg['ack'] = 'data'
        else:
            decoded_msg['id'] = int(msg_id)
            decoded_msg['ack'] = True
    msg_type_id = int(msg_type)
    if msg_type_id in MSG_VALUES:
        decoded_msg['type'] = MSG_VALUES[int(msg_type)]
    else:
        raise Exception('Unknown message type: %s' % msg_type)
    decoded_msg['endpoint'] = endpoint
    if len(split_data) > 3:
        data = split_data[3]
    if msg_type == '0':
        pass
    elif msg_type == '1':
        decoded_msg['qs'] = data
    elif msg_type == '2':
        pass
    elif msg_type == '3':
        decoded_msg['data'] = data
    elif msg_type == '4':
        decoded_msg['data'] = json_loads(data)
    elif msg_type == '5':
        try:
            data = json_loads(data)
        except ValueError, e:
            print (
             'Invalid JSON event message', data)
            decoded_msg['args'] = []
        else:
            decoded_msg['name'] = data.pop('name')
            if 'args' in data:
                decoded_msg['args'] = data['args']
            else:
                decoded_msg['args'] = []
    elif msg_type == '6':
        if '+' in data:
            (ackId, data) = data.split('+')
            decoded_msg['ackId'] = int(ackId)
            decoded_msg['args'] = json_loads(data)
        else:
            decoded_msg['ackId'] = int(data)
            decoded_msg['args'] = []
    elif msg_type == '7':
        if '+' in data:
            (reason, advice) = data.split('+')
            decoded_msg['reason'] = REASONS_VALUES[int(reason)]
            decoded_msg['advice'] = ADVICES_VALUES[int(advice)]
        else:
            decoded_msg['advice'] = ''
            if data != '':
                decoded_msg['reason'] = REASONS_VALUES[int(data)]
            else:
                decoded_msg['reason'] = ''
    elif msg_type == '8':
        pass
    return decoded_msg