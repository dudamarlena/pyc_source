# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/tagging/dict/mgraph.py
# Compiled at: 2020-04-07 05:03:09
# Size of source mod 2**32: 1767 bytes
import os, configparser
from hama.tagging.langutils import Singleton
from .bloomfilter import LookupBloomFilter

class MGraph(metaclass=Singleton):
    __doc__ = 'Class responsible for managing embedded morpheme graphs.\n    \n    Attributes:\n        graph (LookupBloomFilter): Pre-defined morpheme graph.\n    '

    def __init__(self):
        super().__init__()
        self.graph = None

    def __getattr__(self, name):
        """Called when an called attribute does not exist."""
        pass

    def load(self):
        """Loads morpheme graph into memory."""
        if self.graph is None:
            config_path = os.path.join(os.path.dirname(__file__), 'meta/source.ini')
            config = configparser.ConfigParser()
            config.read(config_path)
            fp = config['FILTER_PATH']['g']
            hc = config['HASH_COUNT']['g']
            sz = config['FILTER_SIZE']['g']
            filter = LookupBloomFilter(path=fp, size=(int(sz)),
              hash_count=(int(hc)))
            filter.load()
            self.graph = filter

    def unload(self):
        """Unloads morpheme graph from memory."""
        self.graph = None

    def query(self, seq):
        """See if seq is in morpheme graph.

        Args:
            seq (str): Morpheme graph string.
    
        Returns: 
            bool: True if found, False if not.

         Raises:
            Exception if graph was not initialized
            before with load().
        """
        if self.graph is None:
            raise Exception('Initialize graph before querying!')
        return self.graph.query(seq)