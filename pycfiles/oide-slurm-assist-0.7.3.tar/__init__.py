# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sampedro/Documents/Dev/oide-project/dev-env/local/lib/python2.7/site-packages/oide_slurm_assist-0.0.dev1-py2.7.egg/oideslurm/__init__.py
# Compiled at: 2015-06-01 16:32:06
import os, glob
modules = glob.glob(os.path.dirname(__file__) + '/*.py')
__all__ = [ os.path.basename(f)[:-3] for f in modules ]