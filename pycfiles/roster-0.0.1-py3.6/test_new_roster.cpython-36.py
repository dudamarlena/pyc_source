# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/roster/test_new_roster.py
# Compiled at: 2018-07-20 06:40:54
# Size of source mod 2**32: 433 bytes
import new_roster
tasks = [
 'python ../tests/tasks/add.py', 'python ../tests/tasks/sub.py', 'python ../tests/tasks/mul.py']
roster = new_roster.NewRoster(tasks=tasks)
perform = new_roster.Perform_Task()
print('performing all tasks')
perform.perform_all_tasks()
roster.add_task(tasks=['python tasks/div.py'])
print('performing all tasks')
perform.perform_all_tasks()
roster.db.flushdb()