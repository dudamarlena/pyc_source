# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/support/tnetstrings.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 23, 2011\n\n@package: ally http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nImplementation for handling bytes for tnetstrings, this is made based on the mongrel2.tnetstrings module.\n'

def parse(data):
    payload, payload_type, remain = parse_payload(data)
    if payload_type == '#':
        value = int(payload)
    else:
        if payload_type == '}':
            value = parse_dict(payload)
        else:
            if payload_type == ']':
                value = parse_list(payload)
            else:
                if payload_type == '!':
                    value = payload == 'true'
                else:
                    if payload_type == '^':
                        value = float(payload)
                    else:
                        if payload_type == '~':
                            assert len(payload) == 0, 'Payload must be 0 length for null.'
                            value = None
                        else:
                            if payload_type == ',':
                                value = payload
                            elif not False:
                                raise AssertionError('Invalid payload type: %r' % payload_type)
    return (
     value, remain)


def parse_payload(data):
    assert data, "Invalid data to parse, it's empty."
    length, extra = data.split(':', 1)
    length = int(length)
    payload, extra = extra[:length], extra[length:]
    assert extra, 'No payload type: %r, %r' % (payload, extra)
    payload_type, remain = extra[:1], extra[1:]
    assert len(payload) == length, 'Data is wrong length %d vs %d' % (length, len(payload))
    return (
     payload, payload_type, remain)


def parse_list(data):
    if len(data) == 0:
        return []
    result = []
    value, extra = parse(data)
    result.append(value)
    while extra:
        value, extra = parse(extra)
        result.append(value)

    return result


def parse_pair(data):
    key, extra = parse(data)
    assert extra, 'Unbalanced dictionary store.'
    value, extra = parse(extra)
    return (
     key, value, extra)


def parse_dict(data):
    if len(data) == 0:
        return {}
    key, value, extra = parse_pair(data)
    assert isinstance(key, (str, bytes)), 'Keys can only be strings.'
    result = {key: value}
    while extra:
        key, value, extra = parse_pair(extra)
        result[key] = value

    return result