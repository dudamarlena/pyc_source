# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/trueaccord/pants/scalapb/targets/scalapb_library.py
# Compiled at: 2017-06-26 17:11:03
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
import logging
from pants.backend.jvm.targets.import_jars_mixin import ImportJarsMixin
from pants.backend.jvm.targets.jvm_target import JvmTarget
from pants.base.payload import Payload
from pants.base.payload_field import PrimitiveField
import os

class ScalaPBLibrary(ImportJarsMixin, JvmTarget):
    """A Java library generated from Protocol Buffer IDL files."""

    def __init__(self, payload=None, imports=None, java_conversions=False, flat_package=False, grpc=True, single_line_to_string=False, source_root=None, **kwargs):
        payload = payload or Payload()
        payload.add_fields({b'java_conversions': PrimitiveField(java_conversions), 
           b'flat_package': PrimitiveField(flat_package), 
           b'grpc': PrimitiveField(grpc), 
           b'single_line_to_string': PrimitiveField(single_line_to_string), 
           b'import_specs': PrimitiveField(imports or ()), 
           b'source_root': PrimitiveField(source_root or b'.')})
        super(ScalaPBLibrary, self).__init__(payload=payload, **kwargs)

    @property
    def imported_jar_library_specs(self):
        """List of JarLibrary specs to import.

    Required to implement the ImportJarsMixin.
    """
        return self.payload.import_specs

    @property
    def source_root(self):
        return os.path.normpath(os.path.join(self.target_base, self.payload.source_root))