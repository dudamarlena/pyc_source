# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/station/utils.py
# Compiled at: 2014-09-04 11:46:04
import base64, logging
from pyf.transport.packets import Packet

def base64decoder(flow):
    for item in flow:
        if getattr(item, 'encoded', False) and item.encoding == 'base64':
            item.content = base64.b64decode(item.content)
        yield item


def base64encoder(flow):
    for item in flow:
        if getattr(item, 'content', '') and not getattr(item, 'encoded', False):
            item.content = base64.b64encode(item.content)
            item.encoded = True
            item.encoding = 'base64'
        yield item


def file_to_packets(input_file, buffer=512):
    dat = input_file.read(buffer)
    yield Packet(dict(type='datatransfer', action='start_data', content=dat))
    while True:
        dat = input_file.read(buffer)
        if dat:
            yield Packet(dict(type='datatransfer', action='add_data', content=dat))
        else:
            break

    input_file.close()
    yield Packet(dict(type='datatransfer', action='end_data', content=None))
    return


def handle_data_packet(item, output_file, info_callback=None):
    if info_callback is None:
        info_callback = lambda k, v: logging.debug('%s: %s' % (k, v))
    if item.action == 'start_data':
        info_callback('file_status', 'go')
        output_file.write(item.content)
        return False
    else:
        if item.action == 'add_data':
            output_file.write(item.content)
            return False
        if item.action == 'end_data':
            if item.content:
                output_file.write(item.content)
            info_callback('file_status', 'ok')
            return True
        raise ValueError, 'Action %s unknown' % item.action
        return


def packets_to_file(packet_flow, output_filename, info_callback=None):
    if info_callback is None:
        info_callback = lambda k, v: logging.debug('%s: %s' % (k, v))
    output_file = open(output_filename, 'wb')
    data_finished = False
    for item in packet_flow:
        if handle_data_packet(item, output_file, info_callback):
            data_finished = True
            break

    if not data_finished:
        raise ValueError, 'Bad data ending'
    return