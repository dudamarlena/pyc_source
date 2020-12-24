# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/libreary/scheduler.py
# Compiled at: 2020-03-19 14:48:15
# Size of source mod 2**32: 2676 bytes
import logging
from crontab import CronTab
from typing import List
logger = logging.getLogger(__name__)

class Scheduler:
    __doc__ = '\n    The LIBREary scheduler is responsible for scheduling various kinds of checks of LIBREarys\n\n    It is meant to be interacted with by users. It currently uses cron jobs to schedule access.\n\n    You must use one scheduler per LIBREary.\n\n    This class currently contains the following methods:\n\n    - set_schedule\n    - verify_schedule\n    - show_schedule\n    '

    def __init__(self, config_dir: str):
        try:
            self.crontab = CronTab(user=True)
        except Exception as e:
            try:
                logger.error(f"Could not create Libreary Scheduler. Exception: {e}")
            finally:
                e = None
                del e

    def set_schedule(self, schedule: List[dict]):
        """
        Set a schedule to the scheduler.

        Expects a list of dictionaries, each of which should be structured as follows:
        ```{json}
        {
            "config_dir": "Path to config_directory",
            "levels_to_check": ["list of levels to check"],
            "other_commands":["line here", "line here"],
            "timing": []
        }

        :param schedule - list of dictionaries as described.
        """
        for entry in schedule.items():
            self.add_schedule_job(entry)

    def add_schedule_job(self, schedule_entry: dict):
        """
        Add a single job to the schedule.

        ```{json}
        {
            "config_dir": "Path to config_directory",
            "levels_to_check": ["list of levels to check"],
            "other_commands":["line here", "line here"],
            "timing": [""]
        }
        """
        timing = schedule_entry['timing']
        command = self.build_single_python_command(schedule_entry)
        job = self.crontab.new(command=command)
        job.setall(' '.join(timing))

    def build_single_python_command(self, schedule_entry: dict):
        """
        Build the python command to go in the user's crontab

        :param schedule_entry - dictionary formatted as described below

        Schedule entry format:

        ```{json}
        {
            "config_dir": "Path to config_directory",
            "levels_to_check": ["list of levels to check"],
            "other_commands":["line here", "line here"],
        }
        ```
        """
        base_python_command = f"python3 -c from libreary import Libreary; l = Libreary('{self.config_dir}');"
        for level in schedule_entry['levels_to_check']:
            base_python_command += f"l.check_level('{level}');"
        else:
            base_python_command += ';'.join(schedule_entry['other_commands'])
            return base_python_command