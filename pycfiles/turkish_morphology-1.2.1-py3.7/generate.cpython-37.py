# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/turkish_morphology/generate.py
# Compiled at: 2020-04-06 00:20:11
# Size of source mod 2**32: 3449 bytes
"""Functions to generate Turkish word forms from analysis protobufs."""
import re
from typing import Generator
from turkish_morphology import analysis_pb2
from turkish_morphology import fst
from turkish_morphology import pretty_print
from external.openfst import pywrapfst
_Analysis = analysis_pb2.Analysis
_Ig = analysis_pb2.InflectionalGroup
_SymbolTable = pywrapfst.SymbolTable
_SYMBOLS_REGEX = re.compile('\\(.+?\\[[A-Z\\.,:\\(\\)\\\'\\-\\"`\\$]+?\\]|\\)?\\(\\[[A-Z]+?\\]|-(?:[^\\W\\d_]|\')+?\\[[A-z]+?=[A-z]+?\\]|\\+(?:[^\\W\\d_]|[\'\\.])*?\\[[A-z]+?=[A-z0-9]+?\\]|\\)\\+\\[Proper=(?:True|False)\\]|\\d+(?:\\[[A-Z]+?\\])?|[\\(\\.,]')

def _lower(string: str) -> str:
    """Properly lowercase transforms Turkish string ("İ" -> "i", "I" -> "ı")."""
    return string.replace('İ', 'i').replace('I', 'ı').lower()


def _add_proper(analysis: _Analysis) -> None:
    """Adds the proper feature to the last inflectional group if it is missing."""
    last_ig = analysis.ig[(-1)]
    if last_ig.HasField('proper'):
        return analysis
    with_proper = _Analysis()
    with_proper.CopyFrom(analysis)
    with_proper.ig[(-1)].proper = last_ig.pos == 'NNP'
    return with_proper


def _symbol_indices(analysis: _Analysis, symbol_table: _SymbolTable) -> Generator[(int, None, None)]:
    """Generates the label indices for the symbols that construct the analysis."""
    human_readable = pretty_print.analysis(analysis)
    symbols = _SYMBOLS_REGEX.findall(human_readable)
    yield from map(symbol_table.find, symbols)
    if False:
        yield None


def surface_form(analysis: _Analysis) -> str:
    """Generates surface form for the given morphological analysis.

  This function assumes that input analysis protobuf is structurally
  well-formed, meaning that they should be first validated with
  //turkish_morphology:validate.py.

  Args:
    analysis: morphological analysis of a Turkish word from which surface form
      will be generated.

  Returns:
    Surface form of the Turkish word whose morphological analysis is the
    given morphological analysis. Returns an empty string if a surface form
    cannot be generated from the given morphological analysis.
  """
    symbol_table = fst.ANALYZER.input_symbols()
    symbol_indices = _symbol_indices(_add_proper(analysis), symbol_table)
    input_ = fst.compile(symbol_indices, symbol_table)
    output = fst.compose(fst.ANALYZER, input_)
    if output.start() == -1:
        return ''
    surface_forms = fst.extract_parses(output, output.start(), 'ilabel')
    surface_forms = list(set(map(_lower, surface_forms)))
    return surface_forms[0]