# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/expression/syntax_documentation.py
# Compiled at: 2020-01-31 11:48:19
# Size of source mod 2**32: 7846 bytes
import itertools
from typing import List, Sequence
from exactly_lib.common.help.syntax_contents_structure import SyntaxElementDescription, InvokationVariant, cli_argument_syntax_element_description, invokation_variant_from_args
from exactly_lib.definitions import formatting
from exactly_lib.definitions.entity import syntax_elements, concepts
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.textformat.structure.core import ParagraphItem
from exactly_lib.util.textformat.textformat_parser import TextParser
from .grammar import Grammar, SimpleExpressionDescription, OperatorExpressionDescription, ExpressionWithDescription
from ...definitions.cross_ref.app_cross_ref import SeeAlsoTarget
from ...definitions.entity.syntax_elements import SyntaxElementInfo
from ...util.name_and_value import NameAndValue

def syntax_element_description(grammar: Grammar) -> SyntaxElementDescription:
    return Syntax(grammar).syntax_element_description()


class Syntax:

    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.concept_argument = a.Single(a.Multiplicity.MANDATORY, self.grammar.concept.syntax_element)
        self._tp = TextParser({'symbol_concept': formatting.concept_name_with_formatting(concepts.SYMBOL_CONCEPT_INFO.name), 
         'concept_name': self.grammar.concept.name})

    def syntax_element_description(self) -> SyntaxElementDescription:
        return cli_argument_syntax_element_description(self.grammar.concept.syntax_element, [], self.invokation_variants())

    def invokation_variants(self) -> List[InvokationVariant]:
        return self._invokation_variants_simple() + self._invokation_variants_prefix() + self._invokation_variants_complex() + self._invokation_variants_symbol_ref() + self._invokation_variants_parentheses()

    def global_description(self) -> List[ParagraphItem]:
        return self._tp.fnap(_GLOBAL_DESCRIPTION)

    def syntax_element_descriptions(self) -> List[SyntaxElementDescription]:
        expression_lists = [
         self.grammar.simple_expressions_list,
         self.grammar.prefix_expressions_list,
         self.grammar.complex_expressions_list]
        return list(itertools.chain.from_iterable(map(_seds_for_expr, expression_lists)))

    def see_also_targets(self) -> List[SeeAlsoTarget]:
        """
        :returns: A new list, which may contain duplicate elements.
        """
        expression_dicts = [
         self.grammar.simple_expressions,
         self.grammar.prefix_expressions,
         self.grammar.complex_expressions]
        return list(itertools.chain.from_iterable(map(_see_also_targets_for_expr, expression_dicts)))

    def _invokation_variants_simple(self) -> List[InvokationVariant]:

        def invokation_variant_of(name: str, syntax: SimpleExpressionDescription) -> InvokationVariant:
            name_argument = a.Single(a.Multiplicity.MANDATORY, a.Constant(name))
            all_arguments = [name_argument] + list(syntax.argument_usage_list)
            return invokation_variant_from_args(all_arguments, syntax.description_rest)

        return [invokation_variant_of(expr.name, expr.value.syntax) for expr in self.grammar.simple_expressions_list]

    def _invokation_variants_symbol_ref(self) -> List[InvokationVariant]:

        def invokation_variant(syntax_element: SyntaxElementInfo, description: Sequence[ParagraphItem]) -> InvokationVariant:
            return invokation_variant_from_args([
             a.Single(a.Multiplicity.MANDATORY, syntax_element.argument)], description)

        description_of_sym_ref = self._symbol_ref_description()
        description_of_sym_name = description_of_sym_ref + self._symbol_name_additional_description()
        return [
         invokation_variant(syntax_elements.SYMBOL_REFERENCE_SYNTAX_ELEMENT, description_of_sym_ref),
         invokation_variant(syntax_elements.SYMBOL_NAME_SYNTAX_ELEMENT, description_of_sym_name)]

    def _invokation_variants_complex--- This code section failed: ---

 L. 111         0  LOAD_GLOBAL              str

 L. 112         3  LOAD_GLOBAL              OperatorExpressionDescription
                6  LOAD_GLOBAL              InvokationVariant
                9  LOAD_CONST               ('operator_name', 'syntax', 'return')
               12  LOAD_CLOSURE             'self'
               15  BUILD_TUPLE_1         1 
               18  LOAD_CODE                <code_object invokation_variant_of>
               21  LOAD_STR                 'Syntax._invokation_variants_complex.<locals>.invokation_variant_of'
               24  MAKE_CLOSURE_A_4_0        '0 positional, 0 keyword only, 4 annotated'
               30  STORE_DEREF              'invokation_variant_of'

 L. 120        33  LOAD_CLOSURE             'invokation_variant_of'
               36  BUILD_TUPLE_1         1 
               39  LOAD_LISTCOMP            '<code_object <listcomp>>'
               42  LOAD_STR                 'Syntax._invokation_variants_complex.<locals>.<listcomp>'
               45  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'

 L. 121        48  LOAD_DEREF               'self'
               51  LOAD_ATTR                grammar
               54  LOAD_ATTR                complex_expressions_list
               57  GET_ITER         
               58  CALL_FUNCTION_1       1  '1 positional, 0 named'
               61  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_CLOSURE_A_4_0' instruction at offset 24

    def _invokation_variants_prefix--- This code section failed: ---

 L. 125         0  LOAD_GLOBAL              str

 L. 126         3  LOAD_GLOBAL              OperatorExpressionDescription
                6  LOAD_GLOBAL              InvokationVariant
                9  LOAD_CONST               ('operator_name', 'syntax', 'return')
               12  LOAD_CLOSURE             'self'
               15  BUILD_TUPLE_1         1 
               18  LOAD_CODE                <code_object invokation_variant_of>
               21  LOAD_STR                 'Syntax._invokation_variants_prefix.<locals>.invokation_variant_of'
               24  MAKE_CLOSURE_A_4_0        '0 positional, 0 keyword only, 4 annotated'
               30  STORE_DEREF              'invokation_variant_of'

 L. 134        33  LOAD_CLOSURE             'invokation_variant_of'
               36  BUILD_TUPLE_1         1 
               39  LOAD_LISTCOMP            '<code_object <listcomp>>'
               42  LOAD_STR                 'Syntax._invokation_variants_prefix.<locals>.<listcomp>'
               45  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'

 L. 135        48  LOAD_DEREF               'self'
               51  LOAD_ATTR                grammar
               54  LOAD_ATTR                prefix_expressions_list
               57  GET_ITER         
               58  CALL_FUNCTION_1       1  '1 positional, 0 named'
               61  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_CLOSURE_A_4_0' instruction at offset 24

    def _invokation_variants_parentheses(self) -> List[InvokationVariant]:
        arguments = [
         a.Single(a.Multiplicity.MANDATORY, a.Constant('(')),
         self.concept_argument,
         a.Single(a.Multiplicity.MANDATORY, a.Constant(')'))]
        iv = invokation_variant_from_args(arguments)
        return [iv]

    def _symbol_ref_description(self) -> List[ParagraphItem]:
        return self._tp.fnap(_SYMBOL_REF_DESCRIPTION)

    def _symbol_name_additional_description(self) -> List[ParagraphItem]:
        return self._tp.fnap(_SYMBOL_NAME_ADDITIONAL_DESCRIPTION)


def _see_also_targets_for_expr(expressions_dict: dict) -> List[SeeAlsoTarget]:
    from_expressions = list(itertools.chain.from_iterable(map(lambda expr: expr.syntax.see_also_targets, expressions_dict.values())))
    always = [
     syntax_elements.SYMBOL_NAME_SYNTAX_ELEMENT.cross_reference_target,
     syntax_elements.SYMBOL_REFERENCE_SYNTAX_ELEMENT.cross_reference_target]
    return from_expressions + always


def _seds_for_expr(expressions: List[NameAndValue[ExpressionWithDescription]]) -> List[SyntaxElementDescription]:
    return list(itertools.chain.from_iterable([expr.value.description().syntax_elements for expr in expressions]))


_SYMBOL_REF_DESCRIPTION = 'Reference to {symbol_concept:a},\nthat must have been defined as {concept_name:a}.\n'
_SYMBOL_NAME_ADDITIONAL_DESCRIPTION = 'A string that is not the name of {concept_name:a}\nis interpreted as the name of {symbol_concept:a}.\n'
_GLOBAL_DESCRIPTION = 'All binary operators have the same precedence.\n\n\nOperators and parentheses must be separated by whitespace.\n'