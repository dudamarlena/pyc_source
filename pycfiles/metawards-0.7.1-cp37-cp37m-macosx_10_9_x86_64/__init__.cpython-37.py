# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/__init__.py
# Compiled at: 2020-04-17 13:53:44
# Size of source mod 2**32: 2494 bytes
"""
.. currentmodule:: metawards

Classes
=======

.. autosummary::
    :toctree: generated/

    Disease
    InputFiles
    Link
    Links
    Network
    Node
    Nodes
    OutputFiles
    Parameters
    Population
    Populations
    VariableSet
    VariableSets

Functions
=========

.. autosummary::
    :toctree: generated/

    get_version_string

"""
__all__ = [
 'get_version_string']
from ._parameters import *
from ._disease import *
from ._inputfiles import *
from ._node import *
from ._link import *
from ._population import *
from ._network import *
from ._outputfiles import *
from ._variableset import *
from ._nodes import *
from ._links import *
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
from . import utils
from . import iterators
from . import extractors
from . import app
from . import analysis

def get_version_string():
    """Return a version string for metawards which can be printed
       into a file or written out to the screen
    """
    from ._version import get_versions
    v = get_versions()
    header = f"metawards version {v['version']}"
    stars = '*' * len(header)

    def center(line, length=48):
        diff = length - len(line)
        if diff <= 0:
            return line
        left = int(diff / 2) * ' '
        return left + line

    newline = '\n'
    stars = center(stars)
    lines = []
    lines.append('')
    lines.append(stars)
    lines.append(center(header))
    lines.append(stars)
    lines.append('')
    lines.append(center('-- Source information --'))
    lines.append(center(f"repository: {v['repository']}"))
    lines.append(center(f"branch: {v['branch']}"))
    lines.append(center(f"revision: {v['full-revisionid']}"))
    lines.append(center(f"last modified: {v['date']}"))
    if v['dirty']:
        lines.append('')
        lines.append('WARNING: This version has not been committed to git,')
        lines.append('WARNING: so you may not be able to recover the original')
        lines.append('WARNING: source code that was used to generate this run!')
    lines.append('')
    lines.append(center('-- Additional information --'))
    lines.append(center('Visit https://metawards.github.io for more information'))
    lines.append(center('about metawards, its authors and its license'))
    lines.append('')
    return newline.join(lines)