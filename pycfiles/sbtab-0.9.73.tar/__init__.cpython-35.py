# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/timo/Desktop/projects/SBtab/pypi_installer/sbtab/__init__.py
# Compiled at: 2018-10-25 03:50:18
# Size of source mod 2**32: 253 bytes
from . import misc
from . import sbml2sbtab
from . import sbtab2sbml
from . import sbtab2html
from . import SBtab
from . import validatorSBtab
from pkg_resources import resource_string
__version__ = resource_string(__name__, 'VERSION').decode('utf-8')