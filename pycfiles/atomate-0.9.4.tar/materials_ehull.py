# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/materials_ehull.py
# Compiled at: 2017-10-28 13:31:09
from __future__ import absolute_import, division, print_function, unicode_literals
from tqdm import tqdm
from matgendb.util import get_database
from pymatgen import MPRester, Structure
from pymatgen.entries.computed_entries import ComputedEntry
from atomate.utils.utils import get_logger
from atomate.vasp.builders.base import AbstractBuilder
logger = get_logger(__name__)
__author__ = b'Anubhav Jain <ajain@lbl.gov>'

class MaterialsEhullBuilder(AbstractBuilder):

    def __init__(self, materials_write, mapi_key=None, update_all=False):
        """
        Starting with an existing materials collection, adds stability information and
        The Materials Project ID.
        Args:
            materials_write: mongodb collection for materials (write access needed)
            mapi_key: (str) Materials API key (if MAPI_KEY env. var. not set)
            update_all: (bool) - if true, updates all docs. If false, only updates
                docs w/o a stability key
        """
        self._materials = materials_write
        self.mpr = MPRester(api_key=mapi_key)
        self.update_all = update_all

    def run(self):
        logger.info(b'MaterialsEhullBuilder starting...')
        self._build_indexes()
        q = {b'thermo.energy': {b'$exists': True}}
        if not self.update_all:
            q[b'stability'] = {b'$exists': False}
        mats = [ m for m in self._materials.find(q, {b'calc_settings': 1, b'structure': 1, b'thermo.energy': 1, b'material_id': 1}) ]
        pbar = tqdm(mats)
        for m in pbar:
            pbar.set_description((b'Processing materials_id: {}').format(m[b'material_id']))
            try:
                params = {}
                for x in [b'is_hubbard', b'hubbards', b'potcar_spec']:
                    params[x] = m[b'calc_settings'][x]

                structure = Structure.from_dict(m[b'structure'])
                energy = m[b'thermo'][b'energy']
                my_entry = ComputedEntry(structure.composition, energy, parameters=params)
                self._materials.update_one({b'material_id': m[b'material_id']}, {b'$set': {b'stability': self.mpr.get_stability([my_entry])[0]}})
                for el, elx in my_entry.composition.items():
                    entries = self.mpr.get_entries(el.symbol, compatible_only=True)
                    min_e = min(entries, key=lambda x: x.energy_per_atom).energy_per_atom
                    energy -= elx * min_e

                self._materials.update_one({b'material_id': m[b'material_id']}, {b'$set': {b'thermo.formation_energy_per_atom': energy / structure.num_sites}})
                mpids = self.mpr.find_structure(structure)
                self._materials.update_one({b'material_id': m[b'material_id']}, {b'$set': {b'mpids': mpids}})
            except:
                import traceback
                logger.exception(b'<---')
                logger.exception((b'There was an error processing material_id: {}').format(m))
                logger.exception(traceback.format_exc())
                logger.exception(b'--->')

        logger.info(b'MaterialsEhullBuilder finished processing.')

    def reset(self):
        logger.info(b'Resetting MaterialsEhullBuilder')
        self._materials.update_many({}, {b'$unset': {b'stability': 1}})
        self._build_indexes()
        logger.info(b'Finished resetting MaterialsEhullBuilder')

    def _build_indexes(self):
        self._materials.create_index(b'stability.e_above_hull')

    @classmethod
    def from_file(cls, db_file, m=b'materials', **kwargs):
        """
        Get a MaterialsEhullBuilder using only a db file
        Args:
            db_file: (str) path to db file
            m: (str) name of "materials" collection
            **kwargs: other parameters to feed into the builder, e.g. mapi_key
        """
        db_write = get_database(db_file, admin=True)
        return cls(db_write[m], **kwargs)