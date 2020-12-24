# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toml/__init__.py
# Compiled at: 2018-10-03 21:56:21
"""Python module which parses and emits TOML.

Released under the MIT license.
"""
from toml import encoder
from toml import decoder
__version__ = '0.10.0'
_spec_ = '0.5.0'
load = decoder.load
loads = decoder.loads
TomlDecoder = decoder.TomlDecoder
TomlDecodeError = decoder.TomlDecodeError
dump = encoder.dump
dumps = encoder.dumps
TomlEncoder = encoder.TomlEncoder
TomlArraySeparatorEncoder = encoder.TomlArraySeparatorEncoder
TomlPreserveInlineDictEncoder = encoder.TomlPreserveInlineDictEncoder