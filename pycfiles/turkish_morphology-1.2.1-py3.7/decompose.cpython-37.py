# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/turkish_morphology/decompose.py
# Compiled at: 2020-03-21 14:08:46
# Size of source mod 2**32: 5797 bytes
"""Functions to parse human-readable analyses into analysis protobuf messages.
"""
import re
from typing import Generator
from turkish_morphology import analysis_pb2
_Affix = analysis_pb2.Affix
_Analysis = analysis_pb2.Analysis
_AFFIX_REGEX = re.compile("[\\+-](?P<meta_morpheme>(?:[^\\W\\d_]|['\\.])*?)\\[(?P<category>[A-z]+?)=(?P<value>[A-z0-9]+?)\\]")
_IG_REGEX = re.compile('\\((?:(?P<root>.+?)\\[(?P<root_pos>[A-Z\\.,:\\(\\)\\\'\\-\\"`\\$]+?)\\]|\\[(?P<derivation_pos>[A-Z\\.,:\\(\\)\\\'\\-\\"`\\$]+?)\\](?P<derivation>-(?:[^\\W\\d_]|\')+?\\[[A-z]+?=[A-z]+?\\])?)(?P<inflections>(?:\\+(?:[^\\W\\d_]|[\'\\.])*?\\[[A-z]+?=[A-z0-9]+?\\])*)\\)(?:\\+\\[Proper=(?P<proper>True|False)\\])?')

class IllformedHumanReadableAnalysisError(Exception):
    __doc__ = 'Raised when a human-readable analysis is structurally ill-formed.'


def _make_affix(human_readable: str) -> Generator[(_Affix, None, None)]:
    """Parses a sequence of human-readable affix analyses into affix protobuf.

  To illustrate, for the given human-readable analysis of below sequence of
  inflectional affixes;

      '+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]'

  this function generates the corresponding affix protobufs;

      affix {
        feature {
          category: 'PersonNumber'
          value: 'A3pl'
        }
        meta_morpheme: 'lAr'
      }
      affix {
        feature {
          category: 'Possessive'
          value: 'P1sg'
        }
        meta_morpheme: 'Hm'
      }

  Args:
    human_readable: human-readable analysis for a sequence of derivational or
      inflectional morphemes (e.g. '-DHk[Derivation=PastNom]' or
      '+lAr[PersonNumber=A3pl]+Hm[Possessive=P1sg]+NDAn[Case=Abl]').

  Yields:
    Affix protobuf messages that are constructed from the human-readable affix
    analyses.
  """
    matches = (m.groupdict() for m in _AFFIX_REGEX.finditer(human_readable))
    for matching in matches:
        affix = _Affix()
        affix.feature.category = matching['category']
        affix.feature.value = matching['value']
        if matching['meta_morpheme']:
            affix.meta_morpheme = matching['meta_morpheme']
        yield affix


def human_readable_analysis(human_readable: str) -> _Analysis:
    """Parses given human-readable analysis into an analysis protobuf.

  To illustrate, for the given human-readable analysis;

      '(Ali[NNP]+lAr[PersonNumber=A3pl]+[Possessive=Pnon]
      +NHn[Case=Gen])+[Proper=True]'

  this function makes the corresponding analysis protobuf;

      inflectional_group {
        pos: 'NNP'
        root {
          morpheme: 'Ali'
        }
        inflection {
          feature {
            category: 'PersonNumber'
            value: 'A3pl'
          }
          meta_morpheme: 'lAr'
        }
        inflection {
          feature {
            category: 'Possessive'
            value: 'Pnon'
          }
        }
        inflection {
          feature {
            category: 'Case'
            value: 'Gen'
          }
          meta_morpheme: 'NHn'
        }
        proper: true
      }

  For the structure of the output analysis protobufs, see:

      //turkish_morphology/analysis.proto

  Args:
    human_readable: human-readable morphological analysis.

  Raises:
    IllformedHumanReadableAnalysisError: given human-readable morphological
      analysis is structurally ill-formed (e.g. missing part-of-speech tag,
      root form, derivational/inflectional morpheme, or feature category/value,
      etc.).

  Returns:
    Analysis protobuf message that is constructed from the human-readable
    analysis.
  """
    if not human_readable:
        raise IllformedHumanReadableAnalysisError('Human-readable analysis is empty.')
    igs = tuple(_IG_REGEX.finditer(human_readable))
    matches = [ig.groupdict() for ig in igs]
    if not (igs and len(human_readable) == igs[(-1)].end() and matches[0]['root'] and matches[0]['root_pos'] and all((m['derivation'] for m in matches[1:])) and all((m['derivation_pos'] for m in matches[1:]))):
        raise IllformedHumanReadableAnalysisError(f"Human-readable analysis is ill-formed: '{human_readable}'")
    analysis = _Analysis()
    for position, matching in enumerate(matches):
        ig = analysis.ig.add()
        if position == 0:
            ig.pos = matching['root_pos']
            ig.root.morpheme = matching['root']
        else:
            ig.pos = matching['derivation_pos']
            derivation = tuple(_make_affix(matching['derivation']))[0]
            ig.derivation.CopyFrom(derivation)
        inflections = _make_affix(matching['inflections'])
        ig.inflection.extend(inflections)
        if matching['proper']:
            ig.proper = matching['proper'] == 'True'

    return analysis