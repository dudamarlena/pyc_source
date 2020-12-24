# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/octodns/yaml.py
# Compiled at: 2020-01-06 16:40:45
from __future__ import absolute_import, division, print_function, unicode_literals
from natsort import natsort_keygen
from yaml import SafeDumper, SafeLoader, load, dump
from yaml.constructor import ConstructorError
_natsort_key = natsort_keygen()

class SortEnforcingLoader(SafeLoader):

    def _construct(self, node):
        self.flatten_mapping(node)
        ret = self.construct_pairs(node)
        keys = [ d[0] for d in ret ]
        keys_sorted = sorted(keys, key=_natsort_key)
        for key in keys:
            expected = keys_sorted.pop(0)
            if key != expected:
                raise ConstructorError(None, None, (b'keys out of order: expected {} got {} at {}').format(expected, key, node.start_mark))

        return dict(ret)


SortEnforcingLoader.add_constructor(SortEnforcingLoader.DEFAULT_MAPPING_TAG, SortEnforcingLoader._construct)

def safe_load(stream, enforce_order=True):
    return load(stream, SortEnforcingLoader if enforce_order else SafeLoader)


class SortingDumper(SafeDumper):
    """
    This sorts keys alphanumerically in a "natural" manner where things with
    the number 2 come before the number 12.

    See https://www.xormedia.com/natural-sort-order-with-zero-padding/ for
    more info
    """

    def _representer(self, data):
        data = sorted(data.items(), key=lambda d: _natsort_key(d[0]))
        return self.represent_mapping(self.DEFAULT_MAPPING_TAG, data)


SortingDumper.add_representer(dict, SortingDumper._representer)

def safe_dump(data, fh, **options):
    kwargs = {b'canonical': False, 
       b'indent': 2, 
       b'default_style': b'', 
       b'default_flow_style': False, 
       b'explicit_start': True}
    kwargs.update(options)
    dump(data, fh, SortingDumper, **kwargs)