# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/blast/AbstractBlastDatabase.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 1606 bytes
import abc, os
from typing import List

class AbstractBlastDatabase:
    fasta_suffix = '.fsa'

    def __init__(self, database_dir):
        """
        Creates a new AbstractBlastDatabase
        :param database_dir: The directory containing the database files.
        """
        __metaclass__ = abc.ABCMeta
        self.database_dir = database_dir

    def get_database_names(self) -> List[str]:
        """
        Get the names of the databases (fasta files) used for BLAST.
        :return: The names of the databases.
        """
        return [f[:-len(self.fasta_suffix)] for f in os.listdir(self.database_dir) if os.path.isfile(os.path.join(self.database_dir, f)) if f.endswith(self.fasta_suffix)]

    def get_path(self, database_name):
        """
        Gets the path to a particular database with the given name.
        :param database_name: The name of the database.
        :return: The path to the database (fasta) file.
        """
        return os.path.join(self.database_dir, database_name + self.fasta_suffix)

    @abc.abstractmethod
    def get_name(self) -> str:
        """
        Gets a name for this blast database implementation.
        :return: A name for this implementation.
        """
        pass

    def get_database_paths(self):
        """
        Gets a list of all database paths.
        :return: A list of all database (fasta file) paths.
        """
        return [self.get_path(x) for x in self.get_database_names()]