# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/stationsapi30/persistence_backend.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2395 bytes
__doc__ = '\nModule containing asbtract classes and a few convenience implementations\nof raw measurements I/O\n'
import os, json
from abc import ABCMeta, abstractmethod
from pyowm.stationsapi30.buffer import Buffer

class PersistenceBackend:
    """PersistenceBackend"""
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
    """JSONPersistenceBackend"""
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