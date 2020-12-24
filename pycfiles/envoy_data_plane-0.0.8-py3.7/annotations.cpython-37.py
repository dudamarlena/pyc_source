# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/udpa/annotations.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 1001 bytes
from dataclasses import dataclass
import betterproto

@dataclass
class MigrateAnnotation(betterproto.Message):
    rename = betterproto.string_field(1)
    rename: str


@dataclass
class FieldMigrateAnnotation(betterproto.Message):
    rename = betterproto.string_field(1)
    rename: str
    oneof_promotion = betterproto.string_field(2)
    oneof_promotion: str


@dataclass
class FileMigrateAnnotation(betterproto.Message):
    move_to_package = betterproto.string_field(2)
    move_to_package: str