# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/config/defaults.py
# Compiled at: 2016-03-23 12:35:00
__doc__ = '\nCreated on 7 dec 2012\n\n@author: rdussurg\n'
import os
from altimetry import __file__ as root_file

class subclass(object):

    def __init__(self, path):
        self.path = path
        self.base = os.path.basename(self.path)
        self.dir = os.path.dirname(self.path)
        self.ext = os.path.splitext(self.base)[1]
        self.set = self.set()

    def set(self):
        return os.path.exists(self.path)


class defaults(object):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        self.rootDir = os.path.dirname(root_file)
        self.etopo = subclass(os.path.join(self.rootDir, ('externals{0}bathy{0}ETOPO2v2g_f4.nc').format(os.path.sep)))
        self.menor = subclass(os.path.join(self.rootDir, ('externals{0}bathy{0}bathy_menor.mat').format(os.path.sep)))
        self.cptDir = os.path.join(self.rootDir, ('externals{0}cpt-city{0}').format(os.path.sep))