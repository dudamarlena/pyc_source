# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/lomtype.py
# Compiled at: 2020-01-13 19:20:07
# Size of source mod 2**32: 6452 bytes
from .basetype import CWLBaseType, IntelligenceContext, Intelligence, MapSubjectPredicate, TypeCheck, Match
from .unknowntype import CWLUnknownType
from .requirementstype import CWLRequirementsType
from langserver.lspobjects import Range
from code.intelligence import LookupNode, IntelligenceNode
from code.intelligencecontext import copy_context
from .lib import ListOrMap
from .typeinference import infer_type
from ..code import workflow

class CWLListOrMapType(CWLBaseType):

    def __init__(self, name, allowed_types, map_sp):
        super().__init__(name)
        self.map_subject_predicate = map_sp
        if not isinstance(allowed_types, list):
            allowed_types = [
             allowed_types]
        self.types = allowed_types
        self.enclosing_workflow = None

    def check(self, node, node_key: str=None, map_sp: MapSubjectPredicate=None) -> TypeCheck:
        if node is None or isinstance(node, (str, list, dict)):
            return TypeCheck(cwl_type=self)
        return TypeCheck(cwl_type=self, match=(Match.No))

    def parse(self, doc_uri: str, node, intel_context: IntelligenceContext, code_intel: Intelligence, problems: list, node_key: str=None, map_sp: MapSubjectPredicate=None, key_range: Range=None, value_range: Range=None, requirements=None):
        obj = ListOrMap(node, key_field=(self.map_subject_predicate.subject), problems=problems)
        if self.name == 'requirements':
            intel_context.requirements = IntelligenceNode(completions=[t.name for t in self.types])
        else:
            if obj.original_obj is None or isinstance(obj.original_obj, str):
                if self.name == 'requirements':
                    ln = LookupNode(loc=value_range)
                    ln.intelligence_node = intel_context.requirements
                    code_intel.add_lookup_node(ln)
                else:
                    if self.name == 'in':
                        if intel_context.workflow_step_intelligence is not None:
                            ln = LookupNode(loc=value_range)
                            ln.intelligence_node = intel_context.workflow_step_intelligence.get_step_inport_completer()
                            code_intel.add_lookup_node(ln)
                    elif self.name == 'output':
                        if intel_context.workflow is not None:
                            ln = LookupNode(loc=value_range)
                            ln.intelligence_node = intel_context.workflow.get_output_source_completer('')
                            code_intel.add_lookup_node(ln)
        for k, v in obj.as_dict.items():
            this_intel_context = copy_context(intel_context)
            this_intel_context.path += [k]
            inferred_type = infer_type(v,
              allowed_types=(self.types),
              key=(k if obj.was_dict else None),
              map_sp=(self.map_subject_predicate if obj.was_dict else None))
            if self.name == 'requirements':
                if isinstance(inferred_type, CWLUnknownType):
                    inferred_type = CWLRequirementsType('requirement', self.types)
            if self.name == 'steps':
                this_intel_context.workflow_step_intelligence = workflow.WFStepIntelligence(step_id=k)
            inferred_type.parse(doc_uri=doc_uri,
              node=v,
              intel_context=this_intel_context,
              code_intel=code_intel,
              problems=problems,
              node_key=(k if obj.was_dict else None),
              map_sp=(self.map_subject_predicate),
              key_range=(obj.get_range_for_id(k)),
              value_range=(obj.get_range_for_value(k)),
              requirements=requirements)
            if self.name == 'steps':
                intel_context.workflow.add_step_intel(k, this_intel_context.workflow_step_intelligence)
            if obj.was_dict:
                if self.name == 'requirements':
                    ln = LookupNode(loc=(obj.get_range_for_id(k)))
                    ln.intelligence_node = intel_context.requirements
                    code_intel.add_lookup_node(ln)
                elif self.name == 'in':
                    wf_step = intel_context.workflow_step_intelligence
                    if wf_step is not None:
                        ln = LookupNode(loc=(obj.get_range_for_id(k)))
                        ln.intelligence_node = wf_step.get_step_inport_completer()
                        code_intel.add_lookup_node(ln)
                        if v is None or isinstance(v, str):
                            ln = LookupNode(loc=(obj.get_range_for_value(k)))
                            ln.intelligence_node = wf_step.get_step_source_completer(v)
                            code_intel.add_lookup_node(ln)
                elif self.name == 'output' and not v is None:
                    if isinstance(v, str):
                        ln = LookupNode(loc=(obj.get_range_for_value(k)))
                        ln.intelligence_node = intel_context.workflow.get_output_source_completer(v)
                        code_intel.add_lookup_node(ln)