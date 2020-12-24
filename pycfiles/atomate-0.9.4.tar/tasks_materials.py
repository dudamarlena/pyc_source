# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/tasks_materials.py
# Compiled at: 2017-08-17 16:27:15
from __future__ import absolute_import, division, print_function, unicode_literals
import os
from datetime import datetime
from pymongo import ReturnDocument
from tqdm import tqdm
from atomate.utils.utils import get_mongolike, get_logger
from atomate.vasp.builders.base import AbstractBuilder
from atomate.vasp.builders.utils import dbid_to_str, dbid_to_int
from matgendb.util import get_database
from monty.serialization import loadfn
from pymatgen import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher, ElementComparator
logger = get_logger(__name__)
__author__ = b'Anubhav Jain <ajain@lbl.gov>'
module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

class TasksMaterialsBuilder(AbstractBuilder):

    def __init__(self, materials_write, counter_write, tasks_read, tasks_prefix=b't', materials_prefix=b'm', query=None):
        """
        Create a materials collection from a tasks collection.

        Args:
            materials_write (pymongo.collection): mongodb collection for materials (write access needed)
            counter_write (pymongo.collection): mongodb collection for counter (write access needed)
            tasks_read (pymongo.collection): mongodb collection for tasks (suggest read-only for safety)
            tasks_prefix (str): a string prefix for tasks, e.g. "t" gives a task_id like "t-132"
            materials_prefix (str): a string prefix to prepend to material_ids
            query (dict): a pymongo query on tasks_read for which tasks to include in the builder
        """
        x = loadfn(os.path.join(module_dir, b'tasks_materials_settings.yaml'))
        self.supported_task_labels = x[b'supported_task_labels']
        self.property_settings = x[b'property_settings']
        self.indexes = x.get(b'indexes', [])
        self.properties_root = x.get(b'properties_root', [])
        self._materials = materials_write
        if self._materials.count() == 0:
            self._build_indexes()
        self._counter = counter_write
        if self._counter.find({b'_id': b'materialid'}).count() == 0:
            self._counter.insert_one({b'_id': b'materialid', b'c': 0})
        self._tasks = tasks_read
        self._t_prefix = tasks_prefix
        self._m_prefix = materials_prefix
        self.query = query

    def run(self):
        logger.info(b'MaterialsTaskBuilder starting...')
        logger.info(b'Initializing list of all new task_ids to process ...')
        previous_task_ids = []
        for m in self._materials.find({}, {b'_tasksbuilder.all_task_ids': 1}):
            previous_task_ids.extend(m[b'_tasksbuilder'][b'all_task_ids'])

        q = {b'state': b'successful', b'task_label': {b'$in': self.supported_task_labels}}
        if self.query:
            common_keys = [ k for k in q.keys() if k in self.query.keys() ]
            if common_keys:
                raise ValueError((b'User query parameter cannot contain key(s): {}').format(common_keys))
            q.update(self.query)
        all_task_ids = [ dbid_to_str(self._t_prefix, t[b'task_id']) for t in self._tasks.find(q, {b'task_id': 1})
                       ]
        task_ids = [ t_id for t_id in all_task_ids if t_id not in previous_task_ids ]
        logger.info((b'There are {} new task_ids to process.').format(len(task_ids)))
        pbar = tqdm(task_ids)
        for t_id in pbar:
            pbar.set_description((b'Processing task_id: {}').format(t_id))
            try:
                taskdoc = self._tasks.find_one({b'task_id': dbid_to_int(t_id)})
                m_id = self._match_material(taskdoc)
                if not m_id:
                    m_id = self._create_new_material(taskdoc)
                self._update_material(m_id, taskdoc)
            except:
                import traceback
                logger.exception(b'<---')
                logger.exception((b'There was an error processing task_id: {}').format(t_id))
                logger.exception(traceback.format_exc())
                logger.exception(b'--->')

        logger.info(b'TasksMaterialsBuilder finished processing.')

    def reset(self):
        logger.info(b'Resetting TasksMaterialsBuilder')
        self._materials.delete_many({})
        self._counter.delete_one({b'_id': b'materialid'})
        self._counter.insert_one({b'_id': b'materialid', b'c': 0})
        self._build_indexes()
        logger.info(b'Finished resetting TasksMaterialsBuilder.')

    @classmethod
    def from_file(cls, db_file, m=b'materials', c=b'counter', t=b'tasks', **kwargs):
        """
        Get a TaskMaterialsBuilder using only a db file.

        Args:
            db_file (str): path to db file
            m (str): name of "materials" collection
            c (str): name of "counter" collection
            t (str): name of "tasks" collection
            **kwargs: other params to put into TasksMaterialsBuilder
        """
        db_write = get_database(db_file, admin=True)
        try:
            db_read = get_database(db_file, admin=False)
            db_read.collection_names()
        except:
            logger.warn(b'Warning: could not get read-only database; using write creds')
            db_read = get_database(db_file, admin=True)

        return cls(db_write[m], db_write[c], db_read[t], **kwargs)

    def _build_indexes(self):
        """
        Create indexes for faster searching
        """
        self._materials.create_index(b'material_id', unique=True)
        for index in self.indexes:
            self._materials.create_index(index)

    def _match_material(self, taskdoc, ltol=0.2, stol=0.3, angle_tol=5):
        """
        Returns the material_id that has the same structure as this task as
         determined by the structure matcher. Returns None if no match.

        Args:
            taskdoc (dict): a JSON-like task document
            ltol (float): StructureMatcher tuning parameter 
            stol (float): StructureMatcher tuning parameter 
            angle_tol (float): StructureMatcher tuning parameter

        Returns:
            (int) matching material_id or None
        """
        formula = taskdoc[b'formula_reduced_abc']
        if b'parent_structure' in taskdoc:
            t_struct = Structure.from_dict(taskdoc[b'parent_structure'][b'structure'])
            q = {b'formula_reduced_abc': formula, b'parent_structure.spacegroup.number': taskdoc[b'parent_structure'][b'spacegroup'][b'number']}
        else:
            sgnum = taskdoc[b'output'][b'spacegroup'][b'number']
            t_struct = Structure.from_dict(taskdoc[b'output'][b'structure'])
            q = {b'formula_reduced_abc': formula, b'sg_number': sgnum}
        for m in self._materials.find(q, {b'parent_structure': 1, b'structure': 1, b'material_id': 1}):
            s_dict = m[b'parent_structure'][b'structure'] if b'parent_structure' in m else m[b'structure']
            m_struct = Structure.from_dict(s_dict)
            sm = StructureMatcher(ltol=ltol, stol=stol, angle_tol=angle_tol, primitive_cell=True, scale=True, attempt_supercell=False, allow_subset=False, comparator=ElementComparator())
            if sm.fit(m_struct, t_struct):
                return m[b'material_id']

        return

    def _create_new_material(self, taskdoc):
        """
        Create a new material document.

        Args:
            taskdoc (dict): a JSON-like task document

        Returns:
            (int) - material_id of the new document
        """
        doc = {b'created_at': datetime.utcnow()}
        doc[b'_tasksbuilder'] = {b'all_task_ids': [], b'prop_metadata': {b'labels': {}, b'task_ids': {}}, b'updated_at': datetime.utcnow()}
        doc[b'spacegroup'] = taskdoc[b'output'][b'spacegroup']
        doc[b'structure'] = taskdoc[b'output'][b'structure']
        doc[b'material_id'] = dbid_to_str(self._m_prefix, self._counter.find_one_and_update({b'_id': b'materialid'}, {b'$inc': {b'c': 1}}, return_document=ReturnDocument.AFTER)[b'c'])
        doc[b'sg_symbol'] = doc[b'spacegroup'][b'symbol']
        doc[b'sg_number'] = doc[b'spacegroup'][b'number']
        for x in [b'formula_anonymous', b'formula_pretty', b'formula_reduced_abc', b'elements',
         b'nelements', b'chemsys']:
            doc[x] = taskdoc[x]

        if b'parent_structure' in taskdoc:
            doc[b'parent_structure'] = taskdoc[b'parent_structure']
            t_struct = Structure.from_dict(taskdoc[b'parent_structure'][b'structure'])
            doc[b'parent_structure'][b'formula_reduced_abc'] = t_struct.composition.reduced_formula
        self._materials.insert_one(doc)
        return doc[b'material_id']

    def _update_material(self, m_id, taskdoc):
        """
        Update a material document based on a new task and using complex logic

        Args:
            m_id (int): material_id for material document to update
            taskdoc (dict): a JSON-like task document
        """
        prop_tlabels = self._materials.find_one({b'material_id': m_id}, {b'_tasksbuilder.prop_metadata.labels': 1})[b'_tasksbuilder'][b'prop_metadata'][b'labels']
        task_label = taskdoc[b'task_label']
        for x in self.property_settings:
            for p in x[b'properties']:
                if task_label in x[b'quality_scores']:
                    t_quality = x[b'quality_scores'][task_label]
                    m_quality = x[b'quality_scores'].get(prop_tlabels.get(p, None), None)
                    if not m_quality or t_quality > m_quality or t_quality == m_quality and taskdoc[b'output'][b'energy_per_atom'] < self._materials.find_one({b'material_id': m_id}, {b'_tasksbuilder': 1})[b'_tasksbuilder'][b'prop_metadata'][b'energies'][p]:
                        materials_key = (b'{}.{}').format(x[b'materials_key'], p) if x.get(b'materials_key') else p
                        tasks_key = (b'{}.{}').format(x[b'tasks_key'], p) if x.get(b'tasks_key') else p
                        self._materials.update_one({b'material_id': m_id}, {b'$set': {materials_key: get_mongolike(taskdoc, tasks_key), (b'_tasksbuilder.prop_metadata.labels.{}').format(p): task_label, 
                                     (b'_tasksbuilder.prop_metadata.task_ids.{}').format(p): dbid_to_str(self._t_prefix, taskdoc[b'task_id']), 
                                     (b'_tasksbuilder.prop_metadata.energies.{}').format(p): taskdoc[b'output'][b'energy_per_atom'], 
                                     b'_tasksbuilder.updated_at': datetime.utcnow()}})
                        if p in self.properties_root:
                            self._materials.update_one({b'material_id': m_id}, {b'$set': {p: get_mongolike(taskdoc, tasks_key)}})

        self._materials.update_one({b'material_id': m_id}, {b'$push': {b'_tasksbuilder.all_task_ids': dbid_to_str(self._t_prefix, taskdoc[b'task_id'])}})
        return