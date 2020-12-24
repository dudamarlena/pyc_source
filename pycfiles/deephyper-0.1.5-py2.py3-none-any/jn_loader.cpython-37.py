# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/plot/jn_loader.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1008 bytes
"""
INSTALL REQUIRED:
    pip install jupyter_contrib_nbextensions
"""
import os, nbformat as nbf

class NbEdit:

    def __init__(self, path_to_jnb, path_to_save='dh-analytics.ipynb'):
        with open(path_to_jnb) as (fp):
            self.nb = nbf.read(fp, 4)
        self.path_to_save = path_to_save

    def setkernel(self, name):
        self.nb['metadata']['kernelspec'] = {'name':name, 
         'display_name':f"Python {name}", 
         'language':'python'}

    def edit(self, n_cell, old, new):
        self.nb['cells'][n_cell]['source'] = self.nb['cells'][n_cell]['source'].replace(old, new)

    def write(self):
        """Write jupyter notebook (.ipynb) file on disk.
        """
        nbf.write(self.nb, self.path_to_save)

    def execute(self):
        """Execute jupyter notebook to generate plots for instance.
        """
        pass