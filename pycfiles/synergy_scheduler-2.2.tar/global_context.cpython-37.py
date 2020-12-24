# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shershen/workspace/scheduler.git/synergy/conf/global_context.py
# Compiled at: 2016-06-29 16:46:55
# Size of source mod 2**32: 1319 bytes
import synergy.db.model.queue_context_entry as queue_context_entry
from synergy.scheduler.scheduler_constants import PROCESS_GC, TOKEN_GC, PROCESS_MX, TOKEN_WERKZEUG, EXCHANGE_UTILS, PROCESS_SCHEDULER, TOKEN_SCHEDULER, QUEUE_UOW_STATUS, QUEUE_JOB_STATUS
from synergy.supervisor.supervisor_constants import PROCESS_SUPERVISOR, TOKEN_SUPERVISOR
from synergy.db.model.daemon_process_entry import daemon_context_entry
process_context = {PROCESS_MX: daemon_context_entry(process_name=PROCESS_MX,
               token=TOKEN_WERKZEUG,
               classname=''), 
 
 PROCESS_GC: daemon_context_entry(process_name=PROCESS_GC,
               token=TOKEN_GC,
               classname=''), 
 
 PROCESS_SCHEDULER: daemon_context_entry(process_name=PROCESS_SCHEDULER,
                      classname='synergy.scheduler.synergy_scheduler.Scheduler.start',
                      token=TOKEN_SCHEDULER), 
 
 PROCESS_SUPERVISOR: daemon_context_entry(process_name=PROCESS_SUPERVISOR,
                       classname='synergy.supervisor.synergy_supervisor.Supervisor.start',
                       token=TOKEN_SUPERVISOR)}
mq_queue_context = {QUEUE_UOW_STATUS: queue_context_entry(exchange=EXCHANGE_UTILS, queue_name=QUEUE_UOW_STATUS), 
 QUEUE_JOB_STATUS: queue_context_entry(exchange=EXCHANGE_UTILS, queue_name=QUEUE_JOB_STATUS)}
timetable_context = {}