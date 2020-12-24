# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/example/handlers/sched/backup_db.py
# Compiled at: 2019-10-06 19:06:26
# Size of source mod 2**32: 338 bytes
import datetime
from lbdrabbit import LbdFuncConfig

def handler(event, context):
    print('now is %s' % datetime.datetime.utcnow())


handler.__lbd_func_config__ = LbdFuncConfig()
handler.__lbd_func_config__.scheduled_job_yes = True
handler.__lbd_func_config__.scheduled_job_expression = 'cron(15 10 * * ? *)'