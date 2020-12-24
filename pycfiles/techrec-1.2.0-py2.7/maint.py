# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/techrec/maint.py
# Compiled at: 2019-11-15 16:32:42
from __future__ import print_function
import sys, logging
from sqlalchemy import inspect
from .config_manager import get_config
from .db import RecDB

def cleanold_cmd(options):
    log = logging.getLogger('cleanold')
    log.debug('starting cleanold[%d]' % options.minage)
    db = RecDB(get_config()['DB_URI'])
    res = db.get_not_completed(options.minage * 3600 * 24)
    count = len(res)
    if options.pretend:
        for rec in res:
            print(rec)

    else:
        for rec in res:
            logging.info('Deleting ' + str(rec))
            s = inspect(rec).session
            s.delete(rec)
            s.commit()

        logging.info('Cleanold complete: %d deleted' % count)
    sys.exit(0)