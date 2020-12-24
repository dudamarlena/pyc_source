# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/file_materials.py
# Compiled at: 2017-08-17 18:10:37
from __future__ import absolute_import, division, print_function, unicode_literals
from tqdm import tqdm
from matgendb.util import get_database
from pymatgen import Composition
from atomate.vasp.builders.base import AbstractBuilder
from atomate.utils.utils import get_logger
logger = get_logger(__name__)
__author__ = b'Anubhav Jain <ajain@lbl.gov>'

class FileMaterialsBuilder(AbstractBuilder):

    def __init__(self, materials_write, data_file, delimiter=b',', header_lines=0):
        """
        Updates the database using a data file. Format of file must be:
        <material_id or formula>, <property>, <value>

        Comment lines should *start* with '#'.

        Args:
            materials_write: mongodb collection for materials (write access needed)
            data_file (str): path to data file
            delimiter (str): delimiter for file parsing
            header_lines (int): number of header lines to skip in data file
        """
        self._materials = materials_write
        self._data_file = data_file
        self._delimiter = delimiter
        self.header_lines = header_lines

    def run(self):
        logger.info(b'Starting FileMaterials Builder.')
        with open(self._data_file, b'rt') as (f):
            line_no = 0
            lines = [ line for line in f ]
            pbar = tqdm(lines)
            for line in pbar:
                line = line.strip()
                if line and not line.startswith(b'#'):
                    line_no += 1
                    if line_no > self.header_lines:
                        line = line.split(self._delimiter)
                        if b'-' in line[0]:
                            search_val = line[0]
                            search_key = b'material_id'
                        else:
                            search_key = b'formula_reduced_abc'
                            search_val = Composition(line[0]).reduced_composition.alphabetical_formula
                        key = line[1]
                        val = line[2]
                        try:
                            val = float(val)
                        except:
                            pass

                        self._materials.update({search_key: search_val}, {b'$set': {key: val}})

        logger.info(b'FileMaterials Builder finished processing')

    def reset(self):
        logger.warn(b'Cannot reset FileMaterials Builder!')

    @classmethod
    def from_file(cls, db_file, data_file=None, m=b'materials', **kwargs):
        """
        Get a FileMaterialsBuilder using only a db file.

        Args:
            db_file (str): path to db file
            data_file (str): path to data file
            m (str): name of "materials" collection
            **kwargs: other parameters to feed into the builder, e.g. mapi_key
        """
        db_write = get_database(db_file, admin=True)
        if data_file:
            return cls(db_write[m], data_file, **kwargs)
        raise ValueError(b'data_file must be provided')