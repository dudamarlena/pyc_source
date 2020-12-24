# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/engines/torsiondrive.py
# Compiled at: 2019-09-20 10:07:20
# Size of source mod 2**32: 989 bytes
from QUBEKit.utils.decorators import for_all_methods, timer_logger
import json

@for_all_methods(timer_logger)
class TorsionDrive:

    def __init__(self, molecule, dihedral, json_filename):
        self.molecule = molecule
        self.dihedral = dihedral
        self.json_filename = json_filename

    def write_json(self):
        """
        Take all necessary info from the molecule object and format it to a json.
        There will be one json per job
        :return: json object
        """
        dihedrals = self.dihedral
        grid_spacing = []
        elements = []
        init_coords = self.molecule.coords
        grid_status = dict()
        scan_info = [
         dihedrals, grid_spacing, elements, init_coords, grid_status]
        with open(self.json_filename, 'w') as (json_file):
            json.dump(scan_info, json_file)

    def execute(self):
        with open(self.json_filename, 'r') as (json_file):
            pass