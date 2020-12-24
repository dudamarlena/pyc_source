# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/data.py
# Compiled at: 2019-12-11 03:55:39
import os
from clocwalk.libs.core.datatype import AttribDict
from clocwalk.libs.core.db_helper import DBHelper
from clocwalk.libs.core.log import LOGGER
from clocwalk.libs.core.settings import PYVERSION
paths = AttribDict()
work_path = [
 '/usr/local/clocwalk/']
home_path = None
if PYVERSION == 2:
    home_path = os.path.expanduser('~')
else:
    from pathlib import Path
    home_path = Path.home()
print home_path
paths.ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
paths.WORK_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
paths.PLUGINS_PATH = os.path.join(paths.ROOT_PATH, 'libs', 'analyzer')
paths.CONFIG_FILE = os.path.join(paths.WORK_PATH, 'conf.yaml')
paths.DB_FILE = os.path.join(paths.WORK_PATH, 'db', 'cve_cpe.db1')
paths.CACHE_PATH = os.path.join(paths.WORK_PATH, 'db', 'cache')
paths.CVE_PATH = os.path.join(paths.WORK_PATH, 'db', 'json')
conf = AttribDict()
conf.verbose = 1
kb = AttribDict()
kb.pluginFunctions = []
kb.cache = None
kb.db = None
logger = LOGGER
try:
    kb.db = DBHelper(paths.DB_FILE)
except Exception as ex:
    logger.warn(ex)