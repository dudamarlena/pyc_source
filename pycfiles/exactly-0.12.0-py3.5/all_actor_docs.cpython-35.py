# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/actors/all_actor_docs.py
# Compiled at: 2017-11-21 07:28:45
# Size of source mod 2**32: 384 bytes
from exactly_lib.help.entities.actors.objects import command_line, file_interpreter_actor, source_interpreter_actor, null_actor
ALL_ACTOR_DOCS = [
 command_line.DOCUMENTATION,
 file_interpreter_actor.DOCUMENTATION,
 source_interpreter_actor.DOCUMENTATION,
 null_actor.DOCUMENTATION]
NAME_2_ACTOR_DOC = dict(map(lambda x: (x.singular_name(), x), ALL_ACTOR_DOCS))