# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/types/entity_configuration.py
# Compiled at: 2017-12-07 08:04:08
# Size of source mod 2**32: 463 bytes
from exactly_lib.help.contents_structure.entity import EntityTypeConfiguration
from exactly_lib.help.entities.types import render
from exactly_lib.help.entities.types.all_types import all_types
from exactly_lib.help.entities.types.contents_structure import types_help
TYPE_ENTITY_CONFIGURATION = EntityTypeConfiguration(types_help(all_types()), render.IndividualTypeConstructor, render.list_render_getter(), render.hierarchy_generator_getter())