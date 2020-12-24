# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/recordtype.py
# Compiled at: 2020-03-10 08:45:40
# Size of source mod 2**32: 10224 bytes
from typing import Dict
from .basetype import CWLBaseType, IntelligenceContext, Intelligence, IntelligenceNode, MapSubjectPredicate, TypeCheck, Match
from .linkedfiletype import CWLLinkedFile
from .linkedschemadeftype import CWLLinkedSchemaDef
from .importincludetype import CWLImportInclude
from .namespacedtype import CWLNameSpacedType
from .expressiontype import CWLExpression
from langserver.lspobjects import Range, CompletionItem, Diagnostic, DiagnosticSeverity
from code.intelligence import LookupNode
from code.intelligencecontext import copy_context
from code.workflow import Workflow
from .typeinference import infer_type
from .lib import get_range_for_key, get_range_for_value
from ..code import workflow
import logging
logger = logging.getLogger(__name__)

class CWLRecordType(CWLBaseType):

    def __init__(self, name, doc, fields):
        super().__init__(name, doc=doc)
        self.fields = fields
        self.required_fields = set((k for k, v in self.fields.items() if v.required))
        self.all_fields = set(self.fields.keys())

    def init(self):
        self.required_fields = set((k for k, v in self.fields.items() if v.required))
        self.all_fields = set(self.fields.keys())

    def check(self, node, node_key: str=None, map_sp: MapSubjectPredicate=None) -> TypeCheck:
        if node is None:
            return TypeCheck(self, Match.No)
        if isinstance(node, dict):
            if '$import' in node:
                return TypeCheck(cwl_type=CWLImportInclude(key='$import', import_context=(self.name)))
            if '$include' in node:
                return TypeCheck(cwl_type=CWLImportInclude(key='$include', import_context=(self.name)))
        required_fields = self.required_fields - {map_sp.subject if map_sp else None}
        if not isinstance(node, dict):
            if map_sp is not None:
                if node_key is not None:
                    if map_sp.predicate in self.required_fields:
                        if len(required_fields) <= 1:
                            return TypeCheck(cwl_type=self)
            return TypeCheck(cwl_type=self, match=(Match.No))
        fields_present = set(node.keys())
        missing_fields = required_fields - fields_present
        extra_fields = fields_present - self.all_fields
        if len(missing_fields):
            return TypeCheck(cwl_type=self, match=(Match.Maybe),
              missing_req_fields=(list(missing_fields)))
        if len(extra_fields):
            return TypeCheck(cwl_type=self, match=(Match.Maybe))
        return TypeCheck(cwl_type=self)

    def parse(self, doc_uri: str, node, intel_context: IntelligenceContext, code_intel: Intelligence, problems: list, node_key: str=None, map_sp: MapSubjectPredicate=None, key_range: Range=None, value_range: Range=None, requirements=None):
        if not isinstance(node, dict):
            if map_sp is not None and map_sp.predicate is not None:
                _field_iterator = [
                 (
                  map_sp.predicate, node)]
            else:
                if node_key is not None:
                    ln = LookupNode(loc=value_range)
                    ln.intelligence_node = self
                    code_intel.add_lookup_node(ln)
                return
        else:
            _field_iterator = node.items()
        field_iterator = _put_this_field_first(_field_iterator, 'requirements')
        field_iterator = _put_this_field_first(field_iterator, 'when')
        extra_inputs_for_when = []
        if self.name == 'Workflow':
            intel_context.workflow = Workflow(node.get('inputs'), node.get('outputs'), node.get('steps'))
        for k, child_node in field_iterator:
            inferred_type = None
            this_intel_context = copy_context(intel_context)
            this_intel_context.path += [k]
            if isinstance(node, dict):
                key_range = get_range_for_key(node, k)
                value_range = get_range_for_value(node, k)
                _field = self.fields.get(k)
                _key_doc = _field.doc or '' if _field is not None else ''
                _key_doc += '\n---\n## Sibling fields\n\n```' + '\n'.join((f"- {k}" for k in self.fields.keys())) + '\n```\n'
                _key_doc += f"\n---\n## {self.name or '-'}\n\n" + (self.doc or '')
                ln = LookupNode(loc=key_range)
                ln.intelligence_node = IntelligenceNode(completions=(list(self.fields.keys())),
                  doc=_key_doc)
                code_intel.add_lookup_node(ln)
            if k == 'class':
                if len(this_intel_context.path) > 2:
                    if this_intel_context.path[(-3)] == 'requirements':
                        ln = LookupNode(loc=value_range)
                        ln.intelligence_node = this_intel_context.requirements
                        code_intel.add_lookup_node(ln)
            if self.name == 'WorkflowStep' and k == 'run' and isinstance(child_node, str):
                inferred_type = CWLLinkedFile(prefix=child_node, extension='.cwl')
            else:
                if self.name == 'InlineJavascriptRequirement' and k == 'expressionLib':
                    code_intel.prepare_expression_lib(child_node)
                    continue
                else:
                    if k in ('$schemas', '$namespaces'):
                        continue
                    else:
                        if ':' in k:
                            inferred_type = CWLNameSpacedType(k)
                        else:
                            field = self.fields.get(k)
                            if field is None:
                                if ':' not in k:
                                    if k[0] != '$':
                                        problems += [
                                         Diagnostic(_range=key_range,
                                           message=f"Unknown field: {k} for type {self.name}",
                                           severity=(DiagnosticSeverity.Warning))]
                                        continue
                                    else:
                                        inferred_type = infer_type(child_node, (field.types), key=k)
                            inferred_type.parse(doc_uri=doc_uri,
                              node=child_node,
                              intel_context=this_intel_context,
                              code_intel=code_intel,
                              problems=problems,
                              node_key=k,
                              map_sp=map_sp,
                              key_range=key_range,
                              value_range=value_range,
                              requirements=requirements)
            if self.name == 'WorkflowStep':
                if k == 'when':
                    if isinstance(inferred_type, CWLExpression):
                        extra_inputs_for_when = inferred_type.guess_inputs()
            if self.name == 'WorkflowOutputParameter':
                if k == 'outputSource':
                    set_port_completers(code_intel, child_node, value_range, this_intel_context.workflow.get_output_source_completer)
            if self.name == 'WorkflowStepInput':
                if k == 'source':
                    set_port_completers(code_intel, child_node, value_range, this_intel_context.workflow_step_intelligence.get_step_source_completer)
            if self.name == 'WorkflowStep':
                if k == 'run':
                    if isinstance(inferred_type, CWLLinkedFile):
                        linked_process = inferred_type.node_dict
                    else:
                        linked_process = child_node
                step_interface = workflow.parse_step_interface(linked_process, problems)
                step_interface.inputs.update(extra_inputs_for_when)
                intel_context.workflow_step_intelligence.set_step_interface(step_interface)

        if self.name == 'Workflow':
            intel_context.workflow.validate_connections(problems=problems)

    def completion(self):
        return [CompletionItem(label=k) for k in self.fields.keys()]


def set_port_completers(code_intel, node, value_range, get_source_completer):
    if isinstance(node, list):
        _iterator = ((_node, get_range_for_value(node, n)) for n, _node in enumerate(node))
    else:
        _iterator = [
         (
          node, value_range)]
    for _node, _value_range in _iterator:
        ln = LookupNode(loc=_value_range)
        ln.intelligence_node = get_source_completer(_node)
        code_intel.add_lookup_node(ln)


class CWLFieldType(CWLBaseType):

    def __init__(self, doc, required, allowed_types):
        super().__init__('a field')
        self.doc = doc
        self.required = required
        if not isinstance(allowed_types, list):
            allowed_types = [
             allowed_types]
        self.types = allowed_types


def _put_this_field_first(_field_iterator, field_name):
    field_iterator = []
    for k, v in _field_iterator:
        if k == field_name:
            field_iterator = [
             (
              k, v)] + field_iterator
        else:
            field_iterator += [(k, v)]

    return field_iterator