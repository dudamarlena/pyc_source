# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/retort/constant.py
# Compiled at: 2017-10-06 15:58:42
# Size of source mod 2**32: 276 bytes
from alembic.operations.ops import DropColumnOp, DropConstraintOp, DropIndexOp, DropTableOp
CONFIG_FILE_NAME = 'retort_conf.py'
DROP_OPERATIONS = (DropTableOp, DropColumnOp, DropIndexOp, DropConstraintOp)
DEFAULT_OPTS = {'compare_type': True, 'compare_server_default': True}