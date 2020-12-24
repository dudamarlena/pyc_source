# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/__init__.py
# Compiled at: 2017-08-29 09:44:06
from ._version import __version_info__, __version__
__author__ = 'Leonhard Neuhaus <neuhaus@lkb.upmc.fr>'
__license__ = 'GNU General Public License 3 (GPLv3)'
import warnings, numpy as np
warnings.simplefilter('ignore', np.VisibleDeprecationWarning)
warnings.simplefilter('error', np.ComplexWarning)
import logging
logging.basicConfig()
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.INFO)
try:
    from IPython import get_ipython
    IPYTHON = get_ipython()
    IPYTHON.magic('gui qt')
except BaseException as e:
    logger.debug('Could not enable IPython gui support: %s.' % e)

from qtpy import QtCore, QtWidgets
APP = QtWidgets.QApplication.instance()
if APP is None:
    logger.debug('Creating new QApplication instance "pyrpl"')
    APP = QtWidgets.QApplication(['pyrpl'])
import os
try:
    user_dir = os.environ['PYRPL_USER_DIR']
except KeyError:
    user_dir = os.path.join(os.path.expanduser('~'), 'pyrpl_user_dir')

user_config_dir = os.path.join(user_dir, 'config')
user_curve_dir = os.path.join(user_dir, 'curve')
user_lockbox_dir = os.path.join(user_dir, 'lockbox')
default_config_dir = os.path.join(os.path.dirname(__file__), 'config')
for path in [user_dir, user_config_dir, user_curve_dir, user_lockbox_dir]:
    if not os.path.isdir(path):
        os.mkdir(path)

from .pyrpl_utils import setloglevel
from .memory import MemoryTree
global_config = MemoryTree('global_config', source='global_config')
try:
    setloglevel(global_config.general.loglevel, loggername=logger.name)
except:
    pass

from .redpitaya import RedPitaya
from .hardware_modules import *
from .attributes import *
from .modules import *
from .curvedb import *
from .pyrpl import *