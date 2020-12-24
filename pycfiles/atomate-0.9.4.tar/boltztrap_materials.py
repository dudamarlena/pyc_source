# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/boltztrap_materials.py
# Compiled at: 2017-06-08 17:43:12
from __future__ import absolute_import, division, print_function, unicode_literals
from tqdm import tqdm
from atomate.utils.utils import get_logger
from matgendb.util import get_database
from pymatgen import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher, ElementComparator
from pymatgen.electronic_structure.boltztrap import BoltztrapAnalyzer
from atomate.vasp.builders.base import AbstractBuilder
logger = get_logger(__name__)
__author__ = b'Anubhav Jain <ajain@lbl.gov>'

class BoltztrapMaterialsBuilder(AbstractBuilder):

    def __init__(self, materials_write, boltztrap_read):
        """
        Update materials collection based on boltztrap collection.

        Args:
            materials_write (pymongo.collection): mongodb collection for materials (write access needed)
            boltztrap_read (pymongo.collection): mongodb collection for boltztrap (suggest read-only for safety)
        """
        self._materials = materials_write
        self._boltztrap = boltztrap_read

    def run(self):
        logger.info(b'BoltztrapMaterialsBuilder starting...')
        logger.info(b'Initializing list of all new boltztrap ids to process ...')
        previous_oids = []
        for m in self._materials.find({}, {b'_boltztrapbuilder.all_object_ids': 1}):
            if b'_boltztrapbuilder' in m:
                previous_oids.extend(m[b'_boltztrapbuilder'][b'all_object_ids'])

        if not previous_oids:
            self._build_indexes()
        all_btrap_ids = [ i[b'_id'] for i in self._boltztrap.find({}, {b'_id': 1}) ]
        new_btrap_ids = [ o_id for o_id in all_btrap_ids if o_id not in previous_oids ]
        logger.info((b'There are {} new boltztrap ids to process.').format(len(new_btrap_ids)))
        pbar = tqdm(new_btrap_ids)
        for o_id in pbar:
            pbar.set_description((b'Processing object_id: {}').format(o_id))
            try:
                doc = self._boltztrap.find_one({b'_id': o_id})
                m_id = self._match_material(doc)
                if not m_id:
                    raise ValueError((b'Cannot find matching material for object_id: {}').format(o_id))
                self._update_material(m_id, doc)
            except:
                import traceback
                logger.exception(b'<---')
                logger.exception((b'There was an error processing task_id: {}').format(o_id))
                logger.exception(traceback.format_exc())
                logger.exception(b'--->')

        logger.info(b'BoltztrapMaterialsBuilder finished processing.')

    def reset(self):
        logger.info(b'Resetting BoltztrapMaterialsBuilder')
        self._materials.update_many({}, {b'$unset': {b'_boltztrapbuilder': 1, b'transport': 1}})
        self._build_indexes()
        logger.info(b'Finished resetting BoltztrapMaterialsBuilder')

    def _match_material(self, doc, ltol=0.2, stol=0.3, angle_tol=5):
        """
        Returns the material_id that has the same structure as this doc as
         determined by the structure matcher. Returns None if no match.

        Args:
            doc (dict): a JSON-like document
            ltol (float): StructureMatcher tuning parameter 
            stol (float): StructureMatcher tuning parameter 
            angle_tol (float): StructureMatcher tuning parameter 

        Returns:
            (int) matching material_id or None
        """
        formula = doc[b'formula_reduced_abc']
        sgnum = doc[b'spacegroup'][b'number']
        for m in self._materials.find({b'formula_reduced_abc': formula, b'sg_number': sgnum}, {b'structure': 1, b'material_id': 1}):
            m_struct = Structure.from_dict(m[b'structure'])
            t_struct = Structure.from_dict(doc[b'structure'])
            sm = StructureMatcher(ltol=ltol, stol=stol, angle_tol=angle_tol, primitive_cell=True, scale=True, attempt_supercell=False, allow_subset=False, comparator=ElementComparator())
            if sm.fit(m_struct, t_struct):
                return m[b'material_id']

        return

    def _update_material(self, m_id, doc):
        """
        Update a material document based on a new task

        Args:
            m_id (int): material_id for material document to update
            doc (dict): a JSON-like Boltztrap document
        """
        bta = BoltztrapAnalyzer.from_dict(doc)
        d = {}
        d[b'zt'] = bta.get_extreme(b'zt')
        d[b'pf'] = bta.get_extreme(b'power factor')
        d[b'seebeck'] = bta.get_extreme(b'seebeck')
        d[b'conductivity'] = bta.get_extreme(b'conductivity')
        d[b'kappa_max'] = bta.get_extreme(b'kappa')
        d[b'kappa_min'] = bta.get_extreme(b'kappa', maximize=False)
        self._materials.update_one({b'material_id': m_id}, {b'$set': {b'transport': d}})
        self._materials.update_one({b'material_id': m_id}, {b'$push': {b'_boltztrapbuilder.all_object_ids': doc[b'_id']}})

    def _build_indexes(self):
        """
        Create indexes for faster searching
        """
        for x in [b'zt', b'pf', b'seebeck', b'conductivity', b'kappa_max', b'kappa_min']:
            self._materials.create_index((b'transport.{}.best.value').format(x))

    @classmethod
    def from_file(cls, db_file, m=b'materials', b=b'boltztrap', **kwargs):
        """
        Get a BoltztrapMaterialsBuilder using only a db file.

        Args:
            db_file (str): path to db file
            m (str): name of "materials" collection
            b (str): name of "boltztrap" collection
            **kwargs: other params to put into BoltztrapMaterialsBuilder
        """
        db_write = get_database(db_file, admin=True)
        try:
            db_read = get_database(db_file, admin=False)
            db_read.collection_names()
        except:
            print(b'Warning: could not get read-only database')
            db_read = get_database(db_file, admin=True)

        return cls(db_write[m], db_read[b], **kwargs)