# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/turkish_morphology/analyze.py
# Compiled at: 2020-04-01 02:23:36
# Size of source mod 2**32: 2113 bytes
"""Functions to morphologically analyze surface forms of Turkish words."""
from typing import List, Optional
from turkish_morphology import fst

def _remove_proper_feature(human_readable: str) -> str:
    """Removes proper feature from human-readable analysis."""
    human_readable = human_readable.replace('+[Proper=False]', '')
    human_readable = human_readable.replace('+[Proper=True]', '')
    return human_readable


def surface_form(surface_form: str, use_proper_feature: Optional[bool]=True) -> List[str]:
    """Morphologically analyses given surface form.

  Args:
    surface_form: surface form of a Turkish word that is to be morphologically
      analyzed.
    use_proper_feature: if true includes 'Proper' feature in the morphological
      analyses.

  Returns:
    Human-readable morphological analyses that the Turkish morphological
    analyzer yields for the given surface form. Returns an empty list if the
    given surface form is not accepted as a Turkish word form.
  """
    symbol_table = fst.ANALYZER.input_symbols()
    input_ = fst.compile(surface_form.encode('utf-8'), symbol_table)
    output = fst.compose(input_, fst.ANALYZER)
    if output.start() == -1:
        return []
    human_readable = fst.extract_parses(output, output.start(), 'olabel', symbol_table)
    if not use_proper_feature:
        human_readable = (_remove_proper_feature(hr) for hr in human_readable)
    return sorted(set(human_readable))