# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\utils\pyPowerSerializer.py
# Compiled at: 2015-01-03 06:36:07
# Size of source mod 2**32: 2965 bytes
import json
from maverig.data import dataHandler

class PyPowerSerializer:
    __doc__ = 'Util class that is used for serialization of the created elements which are depending on the PyPower simulator.\n    Currently refBus, bus, transformer and branch belong to this group of elements.'
    _PyPowerSerializer__PP_JSON_FILE = 'pypower.json'

    def __init__(self):
        """Initialize the PyPowerSerializer holding the pre-formatted JSON object."""
        self.pp_json_object = {'bus': [],  'trafo': [],  'branch': []}

    def serialize(self, elements):
        """Serialize elements to a JSON formatted object.
        :param elements: dict of elements.
        :return: Serialized JSON formatted object.
        """
        self._PyPowerSerializer__build_json(elements)
        return json.dumps(self.pp_json_object, indent=4)

    def serialize_to_file(self, elements):
        """Serialize elements as a JSON formatted stream to a file (.json).
        :param elements: dict of elements.
        :return: Path of the JSON file.
        """
        self._PyPowerSerializer__build_json(elements)
        with open(dataHandler.get_temp_file(self._PyPowerSerializer__PP_JSON_FILE), 'w+') as (f):
            json.dump(self.pp_json_object, f, indent=4)
            f.close()
        return dataHandler.get_temp_file(self._PyPowerSerializer__PP_JSON_FILE)

    def __build_json(self, elements):
        """Build the JSON formatted object.
        :param elements: dict of elements.
        """
        for elem in elements.values():
            if elem['sim_model'] == 'PyPower.RefBus':
                self.pp_json_object['bus'].insert(0, [elem['elem_id'], elem['params']['bus_type'], elem['params']['base_kv']])
            elif elem['sim_model'] == 'PyPower.PQBus':
                self.pp_json_object['bus'].append([
                 elem['elem_id'], elem['params']['bus_type'], elem['params']['base_kv']])
            elif elem['sim_model'] == 'PyPower.Transformer':
                self.pp_json_object['trafo'].append([
                 elem['elem_id'], elem['params']['fbus'], elem['params']['tbus'], elem['params']['ttype'],
                 elem['params']['online'], elem['params']['tap']])
            elif elem['sim_model'] == 'PyPower.Branch':
                self.pp_json_object['branch'].append([
                 elem['elem_id'], elem['params']['fbus'], elem['params']['tbus'], elem['params']['btype'],
                 elem['params']['l'], elem['params']['online']])
                continue