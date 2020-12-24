# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/examples/run_builders.py
# Compiled at: 2017-08-17 18:33:03
"""
To use this file, first modify db.json located in this directory with details for your atomate
output database.
"""
import os
from atomate.vasp.builders.bandgap_estimation import BandgapEstimationBuilder
from atomate.vasp.builders.boltztrap_materials import BoltztrapMaterialsBuilder
from atomate.vasp.builders.dielectric import DielectricBuilder
from atomate.vasp.builders.fix_tasks import FixTasksBuilder
from atomate.vasp.builders.materials_descriptor import MaterialsDescriptorBuilder
from atomate.vasp.builders.materials_ehull import MaterialsEhullBuilder
from atomate.vasp.builders.tags import TagsBuilder
from atomate.vasp.builders.tasks_materials import TasksMaterialsBuilder
__author__ = 'Anubhav Jain <ajain@lbl.gov>'
module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
if __name__ == '__main__':
    dbfile = os.path.join(module_dir, 'db.json')
    build_sequence = [
     FixTasksBuilder, TasksMaterialsBuilder, TagsBuilder,
     MaterialsDescriptorBuilder, BandgapEstimationBuilder, DielectricBuilder,
     BoltztrapMaterialsBuilder]
    for cls in build_sequence:
        b = cls.from_file(dbfile)
        b.run()