# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/turkish_morphology/validate.py
# Compiled at: 2020-03-21 19:20:28
# Size of source mod 2**32: 4957 bytes
"""Functions to validate structural well-formedness of analysis protobufs."""
from typing import Optional
from turkish_morphology import analysis_pb2
_Affix = analysis_pb2.Affix
_Analysis = analysis_pb2.Analysis
_Feature = analysis_pb2.Feature
_Ig = analysis_pb2.InflectionalGroup
_Root = analysis_pb2.Root

class IllformedAnalysisError(Exception):
    __doc__ = 'Raised when a human-readable analysis is structurally ill-formed.'


def _root(root: _Root) -> None:
    """Checks if root is structurally well-formed.

  Args:
    root: root analysis.

  Raises:
    IllformedAnalysisError: root is missing the morpheme field, or its
      morpheme field is set as empty string.
  """
    if not root.HasField('morpheme'):
        raise IllformedAnalysisError(f"Root is missing morpheme: '{root}'")
    if not root.morpheme:
        raise IllformedAnalysisError(f"Root morpheme is empty: '{root}'")


def _feature(feature: _Feature) -> None:
    """Checks if feature is structurally well-formed.

  Args:
    feature: morphological analysis feature.

  Raises:
    IllformedAnalysisError: feature is missing category or value field, or
      its category or value field is set as empty string.
  """
    if not feature.HasField('category'):
        raise IllformedAnalysisError(f"Feature is missing category: '{feature}'")
    else:
        if not feature.category:
            raise IllformedAnalysisError(f"Feature category is empty: '{feature}'")
        if not feature.HasField('value'):
            raise IllformedAnalysisError(f"Feature is missing value: '{feature}'")
        assert feature.value, f"Feature value is empty: '{feature}'"


def _affix(affix: _Affix, derivational: Optional[bool]=False) -> None:
    """Checks if affix is structurally well-formed.

  Args:
    affix: affix analysis.
    derivational: if True, affix corresponds to a derivational feature.

  Raises:
    IllformedAnalysisError: affix is missing the feature field, or affix is
      derivational but its meta_morpheme field is missing or its meta_morpheme
      field is set as empty string.
  """
    if not affix.HasField('feature'):
        raise IllformedAnalysisError(f"Affix is missing feature: '{affix}'")
    else:
        _feature(affix.feature)
        if not derivational:
            return
        if not affix.HasField('meta_morpheme'):
            raise IllformedAnalysisError(f"Derivational affix is missing meta-morpheme: '{affix}'")
        assert affix.meta_morpheme, f"Derivational affix meta-morpheme is empty: '{affix}'"


def _inflectional_group(ig: _Ig, position: int) -> None:
    """Checks if inflectional group is structurally well-formed.

  Args:
    ig: inflectional group analysis.
    position: index of the inflectional group w.r.t. the array of inflectional
      groups of the morphological analysis it belongs to.

  Raises:
    IllformedAnalysisError: inflectional group is missing part-of-speech tag,
      or its part-of-speech tag is set as empty string, or inflectional group
      is the first in morphological analysis and it is missing the root field,
      or inflectional group is derived and it is missing the derivation field.
  """
    if not ig.HasField('pos'):
        raise IllformedAnalysisError(f"Inflectional group {position + 1} is missing part-of-speech tag: '{ig}'")
    if not ig.pos:
        raise IllformedAnalysisError(f"Inflectional group {position + 1} part-of-speech tag is empty: '{ig}'")
    if position == 0:
        if not ig.HasField('root'):
            raise IllformedAnalysisError(f"Inflectional group {position + 1} is missing root: '{ig}'")
        _root(ig.root)
    else:
        if not ig.HasField('derivation'):
            raise IllformedAnalysisError(f"Inflectional group {position + 1} is missing derivational affix: '{ig}'")
        _affix((ig.derivation), derivational=True)
    for inflection in ig.inflection:
        _affix(inflection)


def analysis(analysis: _Analysis) -> None:
    """Checks if analysis protobuf is structurally well-formed.

  Args:
    analysis: morphological analysis.

  Raises:
    IllformedAnalysisError: analysis is missing inflectional groups.
  """
    if not analysis.ig:
        raise IllformedAnalysisError("Analysis is missing inflectional groups: 'analysis'")
    for position, ig in enumerate(analysis.ig):
        _inflectional_group(ig, position)