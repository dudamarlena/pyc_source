# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/trueaccord/pants/scalapb/register.py
# Compiled at: 2017-06-26 17:11:03
from pants.build_graph.build_file_aliases import BuildFileAliases
from trueaccord.pants.scalapb.targets.scalapb_library import ScalaPBLibrary
from trueaccord.pants.scalapb.tasks.scalapb_gen import ScalaPBGen
from pants.goal.task_registrar import TaskRegistrar as task

def build_file_aliases():
    return BuildFileAliases(targets={'scalapb_library': ScalaPBLibrary})


def register_goals():
    task(name='scalapb-gen', action=ScalaPBGen).install('gen')