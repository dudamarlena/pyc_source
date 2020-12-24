# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/realasking/python_project1_environment_pathways_OR_essential_paths/epw/einit.py
# Compiled at: 2017-08-23 22:16:44
# Size of source mod 2**32: 1502 bytes
import sys, os, re, sqlite3, shutil
from epw import cmds

class einit:

    def __init__(self, cfolder, dbf, mname):
        self.home = os.path.expanduser('~')
        self.conf_folder = cfolder
        self.dbfile = dbf
        self.module_name = mname
        self.folder = self.home + '/' + self.conf_folder
        self.df = self.folder + '/' + self.dbfile
        self.bf = self.home + '/BEP'
        self.info = cmds.warnings()
        if not os.path.exists(self.folder):
            os.makedirs((self.folder), exist_ok=True)
        else:
            if not os.path.exists(self.bf):
                os.makedirs((self.bf), exist_ok=True)
            if not os.path.isfile(self.home + '/.modulespath'):
                self.info.Merror()
                exit()
            else:
                setmf = 0
        for modules_folder in re.split(':', os.environ['MODULEPATH']):
            if os.access(modules_folder, os.W_OK):
                setmf = 1
                self.module_file = modules_folder + '/' + self.module_name
                break

        if setmf == 0:
            self.info.Mnerror()
            exit()