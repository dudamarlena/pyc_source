# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/dmap/parser.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 2733 bytes
__doc__ = 'Parser and data extractor for raw DMAP data.\n\nDMAP is basically TLV (see Wikipedia) where the key is a 4 byte ASCII value,\na four byte big endian unsigned int as length and the data as data. So:\n\n  +---------------+------------------+--------------------+\n  | Key (4 bytes) | Length (4 bytes) | Data (Length bytes |\n  +---------------+------------------+--------------------+\n'
from collections import namedtuple
from pyatv import exceptions
from .tags import read_str, read_uint, read_bplist

class DmapTag(namedtuple('DmapTag', ['type', 'name'])):
    """DmapTag"""
    __slots__ = ()

    def __str__(self):
        """Return a string representation of this tag."""
        if isinstance(self.type, str):
            type_name = self.type
        else:
            type_name = self.type.__name__[5:]
        return '[{}, {}]'.format(type_name, self.name)


def _parse(data, data_len, tag_lookup, pos, ctx=None):
    if ctx is None:
        ctx = []
    if pos >= data_len:
        return ctx
    else:
        f_name = read_str(data, pos, 4)
        f_len = read_uint(data, pos + 4, 4)
        pos += 8
        tag = tag_lookup(f_name)
        if tag.type == 'container':
            ctx.append({f_name: _parse(data, (pos + f_len), tag_lookup, pos, ctx=[])})
        else:
            ctx.append({f_name: tag.type(data, pos, f_len)})
        return _parse(data, data_len, tag_lookup, pos + f_len, ctx)


def parse(data, tag_lookup):
    """Parse raw DAAP data and returns it as a python object."""
    return _parse(data, len(data), tag_lookup, 0, [])


def first(dmap_data, *path):
    """Look up a value given a path in some parsed DMAP data."""
    if not (path and isinstance(dmap_data, list)):
        return dmap_data
    for key in dmap_data:
        if path[0] in key:
            return first(key[path[0]], *path[1:])


def pprint(data, tag_lookup, indent=0):
    """Return a pretty formatted string of parsed DMAP data."""
    output = ''
    if isinstance(data, dict):
        for key, value in data.items():
            tag = tag_lookup(key)
            if isinstance(value, (dict, list)) and tag.type is not read_bplist:
                output += '{0}{1}: {2}\n'.format(indent * ' ', key, tag)
                output += pprint(value, tag_lookup, indent + 2)
            else:
                output += '{0}{1}: {2} {3}\n'.format(indent * ' ', key, str(value), tag)

    else:
        if isinstance(data, list):
            for elem in data:
                output += pprint(elem, tag_lookup, indent)

        else:
            raise exceptions.InvalidDmapDataError('invalid dmap data: ' + str(data))
    return output