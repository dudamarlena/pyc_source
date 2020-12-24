# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/opentea/__init__.py
# Compiled at: 2019-07-17 05:02:15
"""
OpenTEA scientific GUI library.
Documentation is hosted at: http://cerfacs.fr/opentea
"""
from __future__ import absolute_import
__author__ = 'Antoine Dautpain'
__credits__ = ['Antoine Dautpain',
 'Guillaume Frichet',
 'Adrien Bonhomme',
 'Corentin Lapeyre',
 'Gregory Hannebique',
 'Franchine Ni',
 'Benjamin Farcy',
 'Luis Segui']
__license__ = 'CeCILL-B'
__version__ = '2.2.0'
__shadate__ = '$Format:%h - %cD$'
__maintainer__ = 'Antoine Dauptain'
__email__ = 'coop@cerfacs.fr'
__status__ = 'Development'
import sys
if sys.hexversion < 33949424 or sys.hexversion > 50331808:
    raise Exception('Must be run with python version at least 2.6.6, and not python 3\nYour version is %i.%i.%i' % sys.version_info[:3])
from .constants import COMMON, TEMP, RUN_CURRENT
from .exceptions import XDRException, XDRnoNodeException, XDRtooManyNodesException, XDRnoFileException, XDRillFormed, XDRUnknownValue, XDRInterrupt, OTException, OTNoNodeException, OTTooManyNodesException, OTNoFileException, OTIllFormed, OTUnknownValue, OTInterrupt
import logging
LOGGER = logging.getLogger()
LOGGER.setLevel('DEBUG')
LOG_LEVEL_FILE = 'DEBUG'
LOG_LEVEL_STREAM = 'DEBUG'
FILE_FORMAT = logging.Formatter('%(asctime)s %(name)s %(levelname)s  %(message)s')
FILE_HANDLER = logging.FileHandler(__name__ + '.log')
FILE_HANDLER.setFormatter(FILE_FORMAT)
FILE_HANDLER.setLevel(LOG_LEVEL_FILE)
LOGGER.addHandler(FILE_HANDLER)
STREAM_FORMAT = logging.Formatter('%(levelname)s  %(message)s')
STREAM_HANDLER = logging.StreamHandler(sys.stdout)
STREAM_HANDLER.setFormatter(STREAM_FORMAT)
STREAM_HANDLER.setLevel(LOG_LEVEL_STREAM)
LOGGER.addHandler(STREAM_HANDLER)
if sys.hexversion < 34015984:
    LOGGER.warning('Your version of python is at least 2 years old.')
    LOGGER.warning('It is unsupported and can cause errors (c.f. issue #27 of AVSP)')
if 'Format' in __shadate__:
    from os.path import dirname, abspath
    import subprocess, inspect
    opentea_dir = dirname(abspath(inspect.getfile(inspect.currentframe())))
    __shadate__ = subprocess.check_output(('cd {} ; git log -1 --format="%h - %cD"').format(opentea_dir), shell=True).strip()
LOGGER.info('Welcome to OpenTEA version ' + __version__)
LOGGER.info('Exact version: ' + __shadate__)
LOGGER.info('Python executable is: ' + sys.executable)
from .path_tools import PathTools
from .dataset import Dataset
from .lazy_methods import pairwise, replace_pattern_in_file, currentnext
from .executor import Executor
from .mesh import Mesh
from .process import BaseProcess, CodeProcess, LibProcess
from .plugin import Plugin
from .wincanvas import WinCanvas