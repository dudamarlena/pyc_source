# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\scheduler.py
# Compiled at: 2011-03-26 09:20:22
"""Module that provides a cron-like task scheduler."""
__all__ = [
 'add_cron_like_task', 'add_interval_task', 'add_monthday_task', 'add_monthly_task', 'add_single_task', 'add_weekday_task', 'add_weekly_task', 'cancel', 'get_task', 'get_tasks', 'rename_task', 'start_scheduler', 'stop_scheduler']
from tgscheduler.scheduler import add_cron_like_task, add_interval_task, add_monthday_task, add_monthly_task, add_single_task, add_weekday_task, add_weekly_task, cancel, get_task, get_tasks, rename_task, start_scheduler, stop_scheduler