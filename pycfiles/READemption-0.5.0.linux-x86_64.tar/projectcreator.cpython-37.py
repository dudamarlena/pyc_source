# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/projectcreator.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 1444 bytes
import os, sys, Bio, matplotlib, pandas as pd, pysam

class ProjectCreator(object):

    def create_root_folder(self, project_name):
        """Create the root folder of a new project with the given name.
        
        Arguments:
        - `project_name`: Name of the project root folder

        """
        if not os.path.exists(project_name):
            os.mkdir(project_name)
        else:
            sys.stderr.write('Cannot create folder "%s"! File/folder with the same name exists already.\n' % project_name)
            sys.exit(2)

    def create_subfolders(self, subfolders):
        """Create required subfolders in the given folder.
        
        Arguments:
        - `project_name`: Name of the project root folder

        """
        for folder in subfolders:
            if not os.path.exists(folder):
                os.mkdir(folder)

    def create_version_file(self, version_file_path, version):
        with open(version_file_path, 'w') as (fh):
            fh.write('READemption version: %s\n' % version)
            fh.write('Python version: %s\n' % sys.version.replace('\n', ' '))
            fh.write('Biopython version: %s\n' % Bio.__version__)
            fh.write('pysam version: %s\n' % pysam.__version__)
            fh.write('matplotlib version: %s\n' % matplotlib.__version__)
            fh.write('pandas version: %s\n' % pd.__version__)