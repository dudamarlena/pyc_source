# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/stationsapi30/persistence_backend.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2395 bytes
"""
Module containing asbtract classes and a few convenience implementations
of raw measurements I/O
"""
import os, json
from abc import ABCMeta, abstractmethod
from pyowm.stationsapi30.buffer import Buffer

class PersistenceBackend:
    __doc__ = '\n    A global abstract class representing an I/O manager for buffer objects containing\n    raw measurements.\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_to_buffer(self):
        """
        Reads meteostation measurement data into a *pyowm.stationsapi30.buffer.Buffer*
        object.

        :returns: a *pyowm.stationsapi30.buffer.Buffer* instance

        """
        pass

    @abstractmethod
    def persist_buffer(self, buffer):
        """
        Saves data contained into a *pyowm.stationsapi30.buffer.Buffer* object
        in a durable form.

        :param buffer: the Buffer object to be persisted
        :type buffer:  *pyowm.stationsapi30.buffer.Buffer* instance

        """
        pass

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)


class JSONPersistenceBackend(PersistenceBackend):
    __doc__ = '\n    A `PersistenceBackend` loading/saving data to a JSON file. Data will be\n    saved as a JSON list, each element being representing data of a\n    *pyowm.stationsapi30.measurement.Measurement* object.\n\n    :param json_file_path: path to the JSON file\n    :type json_file_path: str\n    :param station_id: unique OWM-provided ID of the station whose data is read/saved\n    :type station_id: str\n    '
    _file_path = None
    _station_id = None

    def __init__(self, json_file_path, station_id):
        assert json_file_path is not None
        self._station_id = station_id
        assert os.path.isfile(json_file_path)
        self._file_path = json_file_path

    def load_to_buffer(self):
        if self._station_id is None:
            raise ValueError('No station ID specified')
        result = Buffer(self._station_id)
        with open(self._file_path, 'r') as (f):
            list_of_dicts = json.load(f)
            for _dict in list_of_dicts:
                result.append_from_dict(_dict)

            return result

    def persist_buffer(self, buffer):
        data = list()
        with open(self._file_path, 'w') as (f):
            for msmt in buffer:
                data.append(msmt.to_JSON())

            f.write('[%s]' % ','.join(data))