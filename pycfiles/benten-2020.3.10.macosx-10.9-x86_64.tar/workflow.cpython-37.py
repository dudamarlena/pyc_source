# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/code/workflow.py
# Compiled at: 2020-02-21 13:46:29
# Size of source mod 2**32: 9193 bytes
"""Code to parse step interfaces and connectivity and present results in
a generic way that can be used by code intelligence as well as graph
drawing routines.

We try and be parsimonious about our parsing. On the first pass through,
when we analyze all CWL types, we parse all the individual steps with
this code. We keep references to all the steps in a separate
structure.

In the end we do a global analysis of the workflow, flagging connectivity
problems and building a graph of the workflow. We use this global analysis
to enable port completion. For all of this we reuse the previously extracted
step information.
"""
from typing import Dict
from cwl.lib import get_range_for_value, list_as_map, ListOrMap, normalize_source
from .intelligence import IntelligenceNode, CompletionItem
from langserver.lspobjects import Diagnostic, DiagnosticSeverity
import logging
logger = logging.getLogger(__name__)

class StepInterface:

    def __init__(self, inputs=None, outputs=None):
        self.inputs = inputs or set()
        self.outputs = outputs or set()


class Workflow:

    def __init__(self, inputs, outputs, steps):
        self._inputs = inputs
        self._outputs = outputs
        self._steps = steps
        self.step_intels = {}
        self.wf_inputs = set(list_as_map(inputs, key_field='id', problems=[]).keys())
        self.wf_outputs = set(list_as_map(outputs, key_field='id', problems=[]).keys())

    def validate_connections(self, problems):
        unused_ports = set(self.wf_inputs)
        self.validate_step_connections(unused_ports, problems)
        self.validate_outputs(unused_ports, problems)
        self.flag_unused_inputs(unused_ports, problems)

    def validate_outputs(self, unused_ports, problems):
        outputs = ListOrMap((self._outputs), key_field='id', problems=[])
        for output_id, output in outputs.as_dict.items():
            _validate_source(port=output,
              src_key='outputSource',
              value_range=(outputs.get_range_for_value(output_id)),
              step_id=None,
              workflow=self,
              unused_ports=unused_ports,
              problems=problems)

    def validate_step_connections(self, unused_ports, problems):
        _steps = ListOrMap((self._steps), key_field='id', problems=[])
        for step_id, step in _steps.as_dict.items():
            step_intel = self.step_intels.get(step_id)
            if step_intel and isinstance(step, dict):
                step_intel.validate_connections(ListOrMap((step.get('in')), key_field='id', problems=[]),
                  unused_ports=unused_ports,
                  problems=problems)

    def flag_unused_inputs(self, unused_ports, problems):
        inputs = ListOrMap((self._inputs), key_field='id', problems=[])
        for inp in unused_ports:
            if inp in inputs.as_dict:
                problems += [
                 Diagnostic(_range=(inputs.get_range_for_id(inp)),
                   message='Unused input',
                   severity=(DiagnosticSeverity.Warning))]

    def add_step_intel(self, step_id, step_intel: 'WFStepIntelligence'):
        step_intel.workflow = self
        self.step_intels[step_id] = step_intel

    def get_step_intel(self, step_id):
        return self.step_intels.get(step_id)

    def get_output_source_completer(self, prefix):
        return WFOutputSourceCompleter(self, prefix)


class WFStepIntelligence:

    def __init__(self, step_id):
        super().__init__()
        self.step_id = step_id
        self.step_interface = StepInterface()
        self.workflow = None

    def set_step_interface(self, step_interface: StepInterface):
        self.step_interface = step_interface

    def validate_connections(self, inputs: ListOrMap, unused_ports, problems):
        if self.workflow is None:
            raise RuntimeError('Need to attach workflow first')
        for port_id, port in inputs.as_dict.items():
            if port_id not in self.step_interface.inputs:
                problems += [
                 Diagnostic(_range=(inputs.get_range_for_id(port_id)),
                   message=(f"Expecting one of: {self.step_interface.inputs}" if self.step_interface.inputs else 'No input ports found for this step'),
                   severity=(DiagnosticSeverity.Error))]
            else:
                _validate_source(port=port,
                  src_key='source',
                  value_range=(inputs.get_range_for_value(port_id)),
                  step_id=(self.step_id),
                  workflow=(self.workflow),
                  unused_ports=unused_ports,
                  problems=problems)

    def get_step_inport_completer(self):
        return WFStepInputPortCompleter(inputs=(self.step_interface.inputs))

    def get_step_output_completer(self):
        return WFStepOutputPortCompleter(outputs=(self.step_interface.outputs))

    def get_step_source_completer(self, prefix):
        return PortSourceCompleter(self, prefix)


class WFStepInputPortCompleter(IntelligenceNode):

    def __init__(self, inputs):
        super().__init__(completions=inputs)


class WFStepOutputPortCompleter(IntelligenceNode):

    def __init__(self, outputs):
        super().__init__(completions=outputs)


class PortSourceCompleterBase(IntelligenceNode):

    def __init__(self, prefix):
        super().__init__()
        self.prefix = prefix

    def _completion(self, workflow, step_id=None):
        if '/' not in self.prefix:
            return [CompletionItem(label=_id) for _port in (workflow.step_intels.keys(), workflow.wf_inputs) if _id != step_id for _id in _port]
        src_step, src_port = self.prefix.split('/')
        step_intel = workflow.step_intels.get(src_step)
        if step_intel is not None:
            return [CompletionItem(label=_id) for _id in step_intel.step_interface.outputs]


class PortSourceCompleter(PortSourceCompleterBase):

    def __init__(self, step_intel, prefix):
        super().__init__(prefix)
        self.step_intel = step_intel

    def completion(self):
        return self._completion(workflow=(self.step_intel.workflow), step_id=(self.step_intel.step_id))


class WFOutputSourceCompleter(PortSourceCompleterBase):

    def __init__(self, workflow, prefix):
        super().__init__(prefix)
        self.workflow = workflow

    def completion(self):
        return self._completion(workflow=(self.workflow))


def parse_step_interface(run_field: dict, problems: list):
    step_interface = StepInterface()
    if isinstance(run_field, dict):
        step_interface = StepInterface(inputs=(set(list_as_map((run_field.get('inputs')), key_field='id',
          problems=problems).keys())),
          outputs=(set(list_as_map((run_field.get('outputs')), key_field='id',
          problems=problems).keys())))
    return step_interface


def _validate_source--- This code section failed: ---

 L. 212         0  LOAD_CONST               None
                2  STORE_FAST               'src'

 L. 213         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'port'
                8  LOAD_GLOBAL              str
               10  LOAD_GLOBAL              list
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L. 214        18  LOAD_FAST                'port'
               20  STORE_FAST               'src'
               22  JUMP_FORWARD         62  'to 62'
             24_0  COME_FROM            16  '16'

 L. 215        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'port'
               28  LOAD_GLOBAL              dict
               30  CALL_FUNCTION_2       2  '2 positional arguments'
               32  POP_JUMP_IF_FALSE    62  'to 62'

 L. 216        34  LOAD_FAST                'src_key'
               36  LOAD_FAST                'port'
               38  COMPARE_OP               in
               40  POP_JUMP_IF_FALSE    62  'to 62'

 L. 217        42  LOAD_FAST                'port'
               44  LOAD_METHOD              get
               46  LOAD_FAST                'src_key'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  STORE_FAST               'src'

 L. 218        52  LOAD_GLOBAL              get_range_for_value
               54  LOAD_FAST                'port'
               56  LOAD_FAST                'src_key'
               58  CALL_FUNCTION_2       2  '2 positional arguments'
               60  STORE_FAST               'value_range'
             62_0  COME_FROM            40  '40'
             62_1  COME_FROM            32  '32'
             62_2  COME_FROM            22  '22'

 L. 220        62  LOAD_FAST                'src'
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  POP_JUMP_IF_FALSE    74  'to 74'

 L. 221        70  LOAD_CONST               None
               72  RETURN_VALUE     
             74_0  COME_FROM            68  '68'

 L. 223        74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'src'
               78  LOAD_GLOBAL              list
               80  CALL_FUNCTION_2       2  '2 positional arguments'
               82  POP_JUMP_IF_FALSE   132  'to 132'

 L. 224        84  SETUP_LOOP          160  'to 160'
               86  LOAD_GLOBAL              enumerate
               88  LOAD_FAST                'src'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  GET_ITER         
               94  FOR_ITER            128  'to 128'
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'n'
              100  STORE_FAST               '_src'

 L. 225       102  LOAD_GLOBAL              _validate_one_source
              104  LOAD_FAST                '_src'
              106  LOAD_GLOBAL              get_range_for_value
              108  LOAD_FAST                'src'
              110  LOAD_FAST                'n'
              112  CALL_FUNCTION_2       2  '2 positional arguments'
              114  LOAD_FAST                'step_id'
              116  LOAD_FAST                'workflow'
              118  LOAD_FAST                'unused_ports'
              120  LOAD_FAST                'problems'
              122  CALL_FUNCTION_6       6  '6 positional arguments'
              124  POP_TOP          
              126  JUMP_BACK            94  'to 94'
              128  POP_BLOCK        
              130  JUMP_FORWARD        160  'to 160'
            132_0  COME_FROM            82  '82'

 L. 226       132  LOAD_GLOBAL              isinstance
              134  LOAD_FAST                'src'
              136  LOAD_GLOBAL              str
              138  CALL_FUNCTION_2       2  '2 positional arguments'
              140  POP_JUMP_IF_FALSE   160  'to 160'

 L. 227       142  LOAD_GLOBAL              _validate_one_source
              144  LOAD_FAST                'src'
              146  LOAD_FAST                'value_range'
              148  LOAD_FAST                'step_id'
              150  LOAD_FAST                'workflow'
              152  LOAD_FAST                'unused_ports'
              154  LOAD_FAST                'problems'
              156  CALL_FUNCTION_6       6  '6 positional arguments'
              158  POP_TOP          
            160_0  COME_FROM           140  '140'
            160_1  COME_FROM           130  '130'
            160_2  COME_FROM_LOOP       84  '84'

Parse error at or near `COME_FROM' instruction at offset 160_1


def _validate_one_source(src, value_range, step_id, workflow, unused_ports, problems):
    if src is None:
        return
        src = normalize_source(src)
        unused_ports.discard(src)
        if src in workflow.wf_inputs:
            return
    else:
        err_msg = f"No such workflow input. Expecting one of {workflow.wf_inputs}"
        if isinstance(src, str):
            if '/' in src:
                src_step, src_port = src.split('/')
                err_msg = 'Port can not connect to same step'
                if src_step != step_id:
                    err_msg = f"No step called {src_step}"
                    if src_step in workflow.step_intels:
                        err_msg = f"{src_step} has no port called {src_port}"
                        if src_port in workflow.step_intels[src_step].step_interface.outputs:
                            return
    problems += [
     Diagnostic(_range=value_range,
       message=err_msg,
       severity=(DiagnosticSeverity.Error))]