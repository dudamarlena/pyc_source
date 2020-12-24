# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/code/intelligencecontext.py
# Compiled at: 2019-09-13 12:05:46
# Size of source mod 2**32: 785 bytes
"""This keeps track of any context needed for auto-completions and expression evaluations
This therefore carries """
from typing import List
from dataclasses import dataclass
from .intelligence import IntelligenceNode
from .workflow import Workflow, WFStepIntelligence

@dataclass
class IntelligenceContext:
    path = None
    path: List[str]
    workflow = None
    workflow: Workflow
    workflow_step_intelligence = None
    workflow_step_intelligence: WFStepIntelligence
    requirements = None
    requirements: IntelligenceNode


def copy_context(old: IntelligenceContext) -> IntelligenceContext:
    return IntelligenceContext(path=(list(old.path)),
      workflow=(old.workflow),
      workflow_step_intelligence=(old.workflow_step_intelligence),
      requirements=(old.requirements))