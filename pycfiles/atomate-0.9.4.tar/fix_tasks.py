# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/fix_tasks.py
# Compiled at: 2017-10-13 13:59:48
from __future__ import absolute_import, division, print_function, unicode_literals
from matgendb.util import get_database
from atomate.utils.utils import get_logger
from atomate.vasp.builders.base import AbstractBuilder
logger = get_logger(__name__)
__author__ = b'Anubhav Jain <ajain@lbl.gov>'

class FixTasksBuilder(AbstractBuilder):

    def __init__(self, tasks_write):
        """
        Fix historical problems in the tasks database

        Args:
            tasks_write (pymongo.collection): mongodb collection for tasks (write access needed)
        """
        self._tasks = tasks_write

    def run(self):
        logger.info(b'FixTasksBuilder started.')
        for t in self._tasks.find({b'output.spacegroup.number': {b'$type': 2}}, {b'task_id': 1, b'output': 1}):
            logger.info((b'Fixing string spacegroup, tid: {}').format(t[b'task_id']))
            sg = int(t[b'output'][b'spacegroup'][b'number'])
            self._tasks.update_one({b'task_id': t[b'task_id']}, {b'$set': {b'output.spacegroup.number': sg}})

        for t in self._tasks.find({b'tags': {b'$exists': True}, b'tags.0': {b'$exists': False}}, {b'task_id': 1, b'tags': 1}):
            logger.info((b'Fixing tag (converting to list), tid: {}').format(t[b'task_id']))
            self._tasks.update_one({b'task_id': t[b'task_id']}, {b'$set': {b'tags': [t[b'tags']]}})

        for t in self._tasks.find({b'analysis.delta_volume_percent': {b'$exists': True}, b'analysis.delta_volume_as_percent': {b'$exists': False}}, {b'task_id': 1, b'analysis': 1}):
            logger.info((b'Converting delta_volume_percent to be on a percentage scale, tid: {}').format(t[b'task_id']))
            self._tasks.update_one({b'task_id': t[b'task_id']}, {b'$set': {b'analysis.delta_volume_as_percent': t[b'analysis'][b'delta_volume_percent'] * 100}})

        for t in self._tasks.find({b'analysis.delta_volume_percent': {b'$exists': True}, b'analysis.delta_volume_as_percent': {b'$exists': True}}, {b'task_id': 1}):
            logger.info((b'Removing delta_volume_percent, tid: {}').format(t[b'task_id']))
            self._tasks.update_one({b'task_id': t[b'task_id']}, {b'$unset': {b'analysis.delta_volume_percent': 1}})

        logger.info(b'FixTasksBuilder finished.')

    def reset(self):
        logger.warn(b'Cannot reset FixTasksBuilder!')

    @classmethod
    def from_file(cls, db_file, t=b'tasks', **kwargs):
        """
        Get a FixTasksBuilder using only a db file.

        Args:
            db_file (str): path to db file
            t (str): name of "tasks" collection
            **kwargs: other params to put into FixTasksBuilder
        """
        db_write = get_database(db_file, admin=True)
        return cls(db_write[t], **kwargs)