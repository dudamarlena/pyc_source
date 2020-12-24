# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dear/io/_decoder.py
# Compiled at: 2012-04-27 00:49:21
import os, sys

class DecoderError(RuntimeError):
    pass


class DecoderNotFoundError(DecoderError):
    pass


format2decoder_map = {}
name2decoder_map = {}
decoder_names = [
 'audioread']
path = os.path.dirname(__file__)
sys.path.append(path)
for name in decoder_names:
    try:
        model = __import__('_dc_' + name)
        for fmt in model.support_formats:
            arr = format2decoder_map.setdefault(fmt, [])
            arr.append(model)

        name2decoder_map[name] = model
    except ImportError as ex:
        print ex

sys.path.pop(-1)

def get_decoder(format=None, name=None):
    if not (format or name):
        raise AssertionError
        if format:
            format = format.lower()
            arr = name or format2decoder_map.get(format, [])
            if not arr:
                raise DecoderNotFoundError
            return arr[0]
        model = name2decoder_map.get(name, None)
        if model is None or format not in model.support_formats:
            raise DecoderNotFoundError
        return model
    elif name:
        model = name2decoder_map.get(name, None)
        if model is None:
            raise DecoderNotFoundError
        return model
    return


def open(path):
    name, fmt = path.rsplit('.', 1)
    dc = get_decoder(fmt)
    return dc.Audio(path)