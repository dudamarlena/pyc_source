# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/cli/program_modes/symbol/impl/symbol_usage_resolving.py
# Compiled at: 2019-12-27 10:07:50
# Size of source mod 2**32: 7813 bytes
import itertools
from typing import List, Sequence, Iterator, Dict, Callable, Optional
from exactly_lib.cli.program_modes.symbol.impl.reports.symbol_info import SYMBOL_INFO, SymbolDefinitionInfo, DefinitionsResolver, ContextAnd, SourceInfo
from exactly_lib.symbol.symbol_usage import SymbolDefinition, SymbolUsage, SymbolReference, SymbolUsageVisitor
from exactly_lib.test_case import phase_identifier
from exactly_lib.test_case.phase_identifier import Phase
from exactly_lib.test_case.phases import setup, before_assert, assert_, cleanup
from exactly_lib.test_case.phases.act import ActPhaseInstruction
from exactly_lib.test_case.test_case_doc import TestCaseOfInstructions, ElementWithSourceLocation
from exactly_lib.util import symbol_table
from exactly_lib.util.symbol_table import SymbolTable

class DefinitionsInfoResolverFromTestCase(DefinitionsResolver):

    def __init__(self, test_case: TestCaseOfInstructions, action_to_check: Sequence[SymbolUsage], builtin_symbols: Optional[SymbolTable]):
        self._test_case = test_case
        self._action_to_check = action_to_check
        self._builtin_symbols = symbol_table.symbol_table_from_none_or_value(builtin_symbols)

    def definitions(self) -> Iterator[SymbolDefinitionInfo]:
        usages = list(self.symbol_usages())
        references = self.references(usages)
        user_defined = self._definitions_of_user_defined(usages, references)
        builtin = self._definitions_of_builtins(references)
        return itertools.chain.from_iterable([user_defined, builtin])

    @staticmethod
    def _definitions_of_user_defined--- This code section failed: ---

 L.  37         0  LOAD_GLOBAL              ContextAnd
                3  LOAD_GLOBAL              SymbolDefinition
                6  BINARY_SUBSCR    
                7  LOAD_GLOBAL              SymbolDefinitionInfo
               10  LOAD_CONST               ('definition', 'return')
               13  LOAD_CLOSURE             'references'
               16  BUILD_TUPLE_1         1 
               19  LOAD_CODE                <code_object mk_definition>
               22  LOAD_STR                 'DefinitionsInfoResolverFromTestCase._definitions_of_user_defined.<locals>.mk_definition'
               25  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               31  STORE_FAST               'mk_definition'

 L.  46        34  LOAD_GLOBAL              map
               37  LOAD_FAST                'mk_definition'

 L.  47        40  LOAD_GLOBAL              filter
               43  LOAD_GLOBAL              is_not_none

 L.  48        46  LOAD_GLOBAL              map
               49  LOAD_GLOBAL              _extract_symbol_definition
               52  LOAD_FAST                'usages'
               55  CALL_FUNCTION_2       2  '2 positional, 0 named'
               58  CALL_FUNCTION_2       2  '2 positional, 0 named'
               61  CALL_FUNCTION_2       2  '2 positional, 0 named'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _definitions_of_builtins--- This code section failed: ---

 L.  53         0  LOAD_FAST                'self'
                3  LOAD_ATTR                _builtin_symbols
                6  STORE_DEREF              'builtins'

 L.  55         9  LOAD_GLOBAL              str
               12  LOAD_GLOBAL              SymbolDefinitionInfo
               15  LOAD_CONST               ('name', 'return')
               18  LOAD_CLOSURE             'builtins'
               21  LOAD_CLOSURE             'references'
               24  BUILD_TUPLE_2         2 
               27  LOAD_CODE                <code_object mk_definition>
               30  LOAD_STR                 'DefinitionsInfoResolverFromTestCase._definitions_of_builtins.<locals>.mk_definition'
               33  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               39  STORE_DEREF              'mk_definition'

 L.  60        42  LOAD_GLOBAL              iter

 L.  61        45  LOAD_CLOSURE             'mk_definition'
               48  BUILD_TUPLE_1         1 
               51  LOAD_LISTCOMP            '<code_object <listcomp>>'
               54  LOAD_STR                 'DefinitionsInfoResolverFromTestCase._definitions_of_builtins.<locals>.<listcomp>'
               57  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'

 L.  62        60  LOAD_DEREF               'builtins'
               63  LOAD_ATTR                names_set
               66  GET_ITER         
               67  CALL_FUNCTION_1       1  '1 positional, 0 named'
               70  CALL_FUNCTION_1       1  '1 positional, 0 named'
               73  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_CLOSURE_A_3_0' instruction at offset 33

    def symbol_usages(self) -> Iterator[ContextAnd[SymbolUsage]]:
        return itertools.chain.from_iterable([
         _symbol_usages_from(phase_identifier.SETUP, self._test_case.setup_phase, setup.get_symbol_usages),
         self._act_phase_symbol_usages(),
         _symbol_usages_from(phase_identifier.BEFORE_ASSERT, self._test_case.before_assert_phase, before_assert.get_symbol_usages),
         _symbol_usages_from(phase_identifier.ASSERT, self._test_case.assert_phase, assert_.get_symbol_usages),
         _symbol_usages_from(phase_identifier.CLEANUP, self._test_case.cleanup_phase, cleanup.get_symbol_usages)])

    def _act_phase_symbol_usages--- This code section failed: ---

 L.  81         0  LOAD_GLOBAL              _UsagesExtractor
                3  CALL_FUNCTION_0       0  '0 positional, 0 named'
                6  STORE_DEREF              'usages_extractor'

 L.  82         9  LOAD_FAST                'self'
               12  LOAD_ATTR                _act_phase_source_info
               15  CALL_FUNCTION_0       0  '0 positional, 0 named'
               18  STORE_DEREF              'source_info'

 L.  84        21  LOAD_GLOBAL              SymbolUsage
               24  LOAD_GLOBAL              ContextAnd
               27  LOAD_GLOBAL              SymbolUsage
               30  BINARY_SUBSCR    
               31  LOAD_CONST               ('usage', 'return')
               34  LOAD_CLOSURE             'source_info'
               37  BUILD_TUPLE_1         1 
               40  LOAD_CODE                <code_object mk_atc_sym_usage>
               43  LOAD_STR                 'DefinitionsInfoResolverFromTestCase._act_phase_symbol_usages.<locals>.mk_atc_sym_usage'
               46  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               52  STORE_FAST               'mk_atc_sym_usage'

 L.  89        55  LOAD_GLOBAL              map

 L.  90        58  LOAD_FAST                'mk_atc_sym_usage'

 L.  91        61  LOAD_GLOBAL              itertools
               64  LOAD_ATTR                chain
               67  LOAD_ATTR                from_iterable

 L.  92        70  LOAD_CLOSURE             'usages_extractor'
               73  BUILD_TUPLE_1         1 
               76  LOAD_LISTCOMP            '<code_object <listcomp>>'
               79  LOAD_STR                 'DefinitionsInfoResolverFromTestCase._act_phase_symbol_usages.<locals>.<listcomp>'
               82  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'

 L.  93        85  LOAD_FAST                'self'
               88  LOAD_ATTR                _action_to_check
               91  GET_ITER         
               92  CALL_FUNCTION_1       1  '1 positional, 0 named'
               95  CALL_FUNCTION_1       1  '1 positional, 0 named'
               98  CALL_FUNCTION_2       2  '2 positional, 0 named'
              101  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_CLOSURE_A_3_0' instruction at offset 46

    def _act_phase_source_info(self) -> SourceInfo:

        def instruction_source_lines(instruction: ElementWithSourceLocation[ActPhaseInstruction]) -> Sequence[str]:
            return instruction.value.source_code().lines

        source_lines = list(itertools.chain.from_iterable(map(instruction_source_lines, self._test_case.act_phase)))
        if source_lines:
            return SourceInfo.of_lines(source_lines)
        else:
            return SourceInfo.empty()

    @staticmethod
    def references(usages: List[ContextAnd[SymbolUsage]]) -> Dict[(str, List[ContextAnd[SymbolReference]])]:
        context_and_reference_iter = filter(is_not_none, map(_extract_symbol_reference, usages))
        ret_val = {}
        for context_and_reference in context_and_reference_iter:
            name = context_and_reference.value().name
            refs_for_name = ret_val.setdefault(name, [])
            refs_for_name.append(context_and_reference)

        return ret_val


def _symbol_usages_from--- This code section failed: ---

 L. 132         0  LOAD_GLOBAL              _UsagesExtractor
                3  CALL_FUNCTION_0       0  '0 positional, 0 named'
                6  STORE_DEREF              'usages_extractor'

 L. 134         9  LOAD_GLOBAL              SYMBOL_INFO
               12  LOAD_GLOBAL              Iterator
               15  LOAD_GLOBAL              SymbolUsage
               18  BINARY_SUBSCR    
               19  LOAD_CONST               ('symbol_info', 'return')
               22  LOAD_CLOSURE             'symbol_usages_getter'
               25  LOAD_CLOSURE             'usages_extractor'
               28  BUILD_TUPLE_2         2 
               31  LOAD_CODE                <code_object get_direct_and_indirect_symbol_usages>
               34  LOAD_STR                 '_symbol_usages_from.<locals>.get_direct_and_indirect_symbol_usages'
               37  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               43  STORE_DEREF              'get_direct_and_indirect_symbol_usages'

 L. 141        46  LOAD_CLOSURE             'get_direct_and_indirect_symbol_usages'
               49  BUILD_TUPLE_1         1 
               52  LOAD_LISTCOMP            '<code_object <listcomp>>'
               55  LOAD_STR                 '_symbol_usages_from.<locals>.<listcomp>'
               58  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'

 L. 149        61  LOAD_FAST                'elements'
               64  GET_ITER         
               65  CALL_FUNCTION_1       1  '1 positional, 0 named'
               68  STORE_FAST               'symbol_usages_sequence_list'

 L. 152        71  LOAD_GLOBAL              ElementWithSourceLocation
               74  LOAD_GLOBAL              SymbolUsage
               77  BINARY_SUBSCR    
               78  LOAD_GLOBAL              ContextAnd
               81  LOAD_GLOBAL              SymbolUsage
               84  BINARY_SUBSCR    
               85  LOAD_CONST               ('element', 'return')
               88  LOAD_CLOSURE             'phase'
               91  BUILD_TUPLE_1         1 
               94  LOAD_CODE                <code_object mk_item>
               97  LOAD_STR                 '_symbol_usages_from.<locals>.mk_item'
              100  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
              106  STORE_FAST               'mk_item'

 L. 157       109  LOAD_GLOBAL              map
              112  LOAD_FAST                'mk_item'

 L. 158       115  LOAD_GLOBAL              itertools
              118  LOAD_ATTR                chain
              121  LOAD_ATTR                from_iterable
              124  LOAD_FAST                'symbol_usages_sequence_list'
              127  CALL_FUNCTION_1       1  '1 positional, 0 named'
              130  CALL_FUNCTION_2       2  '2 positional, 0 named'
              133  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_CLOSURE_A_3_0' instruction at offset 37


def _extract_symbol_definition(usage: ContextAnd[SymbolUsage]) -> Optional[ContextAnd[SymbolDefinition]]:
    value = usage.value()
    if isinstance(value, SymbolDefinition):
        return ContextAnd(usage.phase(), usage.source_info(), value)
    else:
        return


def _extract_symbol_reference(context_and_usage: ContextAnd[SymbolUsage]) -> Optional[ContextAnd[SymbolReference]]:
    usage = context_and_usage.value()
    if isinstance(usage, SymbolReference):
        return ContextAnd(context_and_usage.phase(), context_and_usage.source_info(), usage)
    else:
        return


def is_not_none(x) -> bool:
    return x is not None


class _UsagesExtractor(SymbolUsageVisitor):

    def _visit_definition(self, definition: SymbolDefinition) -> List[SymbolUsage]:
        return [definition] + list(definition.references)

    def _visit_reference(self, reference: SymbolReference) -> List[SymbolUsage]:
        return [
         reference]