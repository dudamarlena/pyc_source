# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patri/MODPIN/modpin/./src/SBI/beans/StorableObject.py
# Compiled at: 2020-04-28 10:16:58
"""StorableObject

author: jbonet
date:   01/2013

@oliva's lab
"""
from abc import ABCMeta
try:
    import cPickle as pickle
except:
    import pickle

import sys
from . import File
from SBI import SBIglobals

class StorableObject(object):
    """StorableObject is an abstract "dumping" class.

        This means that it is basically usefull for those who would like to extend this library.
        Basically, it gives the object the hability to be "dumped" on disk and be recovered afterwards.

        [AS AN ABSTRACT OBJECT, IT DOES NOT HAVE A CONSTRUCTOR]

        Methods:
            - dump(): Stores the object into a file
                        - object_file (string): Name for the output file
                                                @Mandatory
                        - overwrite (bool):     Overwrite previous file of the same name
                      @Raises FileError

            > load(): Retrieves the object from a python object file
                        - object_file (string): Name of the file containing the object
                                                @Mandatory
                      @Returns the loaded object.
                      @staticmethod: can be called without any instance declared
                      @Raises FileError
                      
        Requirements:
            * abc, cPickle/pickle, sys
            < SBI.beans.File
            < SBI.SBIglobals
    """
    __metaclass__ = ABCMeta

    def dump(self, object_file, overwrite=None):
        """
            - dump(): Stores the object into a file
                        - object_file (string): Name for the output file
                                                @Mandatory
                        - overwrite (bool):     Overwrite previous file of the same name
                      @Raises FileError
        """
        SBIglobals.alert('verbose', self, ('Writting object to file {0}').format(object_file))
        dumpFile = File(file_name=object_file, action='wb', overwrite=overwrite)
        pickle.dump(self, dumpFile.descriptor)
        dumpFile.close()

    @staticmethod
    def load(object_file):
        """
            > load(): Retrieves the object from a python object file
                        - object_file (string): Name of the file containing the object
                                                @Mandatory
                      @Returns the loaded object.
                      @staticmethod: can be called without any instance declared
                      @Raises FileError
        """
        SBIglobals.alert('verbose', StorableObject, ('Preparing to load object from file {0}').format(object_file))
        Object = None
        loadFile = File(file_name=object_file, action='rb')
        Object = pickle.load(loadFile.descriptor)
        loadFile.close()
        return Object