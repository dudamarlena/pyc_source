# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parsimony/persistence/object_store.py
# Compiled at: 2014-12-21 11:18:27
# Size of source mod 2**32: 1816 bytes
"""Ways to store objects."""
import pickle, string, os.path
from parsimony.configuration import parsimony_directory, context_name
from . import Store

class PickleStore(Store):
    __doc__ = 'Store that uses the local file system and pickle as the underlying mechanism.\n\n    '

    def __init__(self, key, base_directory=None):
        """Constructor.

        :param key: key of this store
        :param base_directory: optional. Default None. If None, the parsimony configuration directory is used.
        """
        if base_directory is None:
            base_directory = parsimony_directory()
        self._directory = os.path.join(base_directory, context_name())
        if not os.path.exists(self._directory):
            os.makedirs(self._directory)
        self._store_location = self._generate_store_location(self._directory, key)
        super().__init__(key)

    def read(self):
        """Pickle load the stored value
        """
        with open(self._store_location, 'rb') as (result_file):
            result = pickle.load(result_file)
        return result

    def write(self, value):
        """Dump the value to the pickle store

        :param value: value to dump
        """
        with open(self._store_location, 'wb') as (result_file):
            pickle.dump(value, result_file)

    def _generate_store_location(self, directory, key):
        """Generates a location in the pickle directory to store to

        :param directory: base directory
        :param key: value key, necessary because this is called in the constructor
        """
        valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
        file_name = ''.join((c if c in valid_chars else '_') for c in key)
        return os.path.join(directory, file_name)