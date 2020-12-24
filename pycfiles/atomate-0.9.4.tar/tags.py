# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/tags.py
# Compiled at: 2017-08-17 18:39:33
from __future__ import absolute_import, division, print_function, unicode_literals
from tqdm import tqdm
from atomate.vasp.builders.utils import dbid_to_int, dbid_to_str
from matgendb.util import get_database
from atomate.utils.utils import get_logger
from atomate.vasp.builders.tasks_materials import TasksMaterialsBuilder
from atomate.vasp.builders.base import AbstractBuilder
logger = get_logger(__name__)
__author__ = b'Alireza Faghanina <albalu@lbl.gov>, Anubhav Jain <ajain@lbl.gov>'

class TagsBuilder(AbstractBuilder):

    def __init__(self, materials_write, tasks_read, tasks_prefix=b't'):
        """
        Starting with an existing materials collection, searches all its component tasks for 
        the "tags" and key in the tasks collection and copies them to the materials collection.
        Thus, the "tags" for a material will be the union of all the tags for its component tasks.

        Args:
            materials_write (pymongo.collection): materials collection with write access.
            tasks_read (pymongo.collection): read-only(for safety) tasks collection.
            tasks_prefix (str): the string prefix for tasks, e.g. "t" for a task_id like "t-132"

        """
        self._materials = materials_write
        self._tasks = tasks_read
        self._tasks_prefix = tasks_prefix

    def run(self):
        logger.info(b'TagsBuilder starting...')
        self._build_indexes()
        logger.info(b'Initializing list of all new task_ids to process ...')
        previous_task_ids = []
        for m in self._materials.find({b'_tagsbuilder': {b'$exists': True}}, {b'_tagsbuilder.all_task_ids': 1}):
            previous_task_ids.extend(m[b'_tagsbuilder'][b'all_task_ids'])

        previous_task_ids = [ dbid_to_int(t) for t in previous_task_ids ]
        q = {b'tags': {b'$exists': True}, b'task_id': {b'$nin': previous_task_ids}, b'state': b'successful'}
        tasks = [ t for t in self._tasks.find(q, {b'task_id': 1, b'tags': 1}) ]
        pbar = tqdm(tasks)
        for t in pbar:
            try:
                pbar.set_description((b'Processing task_id: {}').format(t[b'task_id']))
                m = self._materials.find_one({b'_tasksbuilder.all_task_ids': dbid_to_str(self._tasks_prefix, t[b'task_id'])}, {b'material_id': 1, b'tags': 1, b'_tagsbuilder': 1})
                if m:
                    all_tags = t[b'tags']
                    if b'tags' in m and m[b'tags']:
                        all_tags.extend(m[b'tags'])
                    all_tasks = [dbid_to_str(self._tasks_prefix, t[b'task_id'])]
                    if b'_tagsbuilder' in m:
                        all_tasks.extend(m[b'_tagsbuilder'][b'all_task_ids'])
                    all_tags = list(set(all_tags))
                    self._materials.update_one({b'material_id': m[b'material_id']}, {b'$set': {b'tags': all_tags, b'_tagsbuilder.all_task_ids': all_tasks}})
            except:
                import traceback
                logger.exception(b'<---')
                logger.exception((b'There was an error processing task_id: {}').format(t[b'task_id']))
                logger.exception(traceback.format_exc())
                logger.exception(b'--->')

        logger.info(b'TagsBuilder finished processing.')

    def reset(self):
        logger.info(b'Resetting TagsBuilder')
        self._materials.update_many({}, {b'$unset': {b'tags': 1, b'_tagsbuilder': 1}})
        self._build_indexes()
        logger.info(b'Finished resetting TagsBuilder')

    def _build_indexes(self):
        self._materials.create_index(b'tags')
        self._materials.create_index(b'_tagsbuilder.all_task_ids')

    @classmethod
    def from_file(cls, db_file, m=b'materials', t=b'tasks', **kwargs):
        """
        Get a TagsCollector using only a db file.

        Args:
            db_file (str): path to db file
            m (str): name of "materials" collection
            **kwargs: other parameters to feed into the builder, e.g. update_all
        """
        db_write = get_database(db_file, admin=True)
        try:
            db_read = get_database(db_file, admin=False)
            db_read.collection_names()
        except:
            print(b'Warning: could not get read-only database; using write creds')
            db_read = get_database(db_file, admin=True)

        return cls(db_write[m], db_read[t], **kwargs)