# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/projectManager.py
# Compiled at: 2011-12-25 05:31:43
import os, shutil
from os.path import basename, join as pjoin, dirname, abspath
from ioUtils import copy_directory
from consoleHelpers import ask
from config import proj_settings as settings
from config import INSTALL_LOC as rooot
installPath = pjoin(rooot, 'baseProject')

def newProject(toPath):
    doCopy = True
    if os.path.exists(toPath):
        overwrite = ask('Path Already Exists!, Do you want to overwrite?')
        if overwrite:
            shutil.rmtree(toPath)
        else:
            doCopy = False
    if doCopy:
        os.makedirs(toPath)
        os.makedirs(pjoin(toPath, 'src'))
        copy_directory(installPath, pjoin(toPath, 'src'), ['.git'], ['.gitignore', '.pyc', '.InRoot'])
        str = open(pjoin(toPath, 'src', 'app.yaml'), 'r').read()
        str = str.replace('{{appname}}', basename(toPath).lower())
        f = open(os.path.join(toPath, 'src', 'app.yaml'), 'w')
        f.write(str)
        f.close()
        str = open(pjoin(rooot, 'halicea_manage.py'), 'r').read()
        str = str.replace('{{hal_path}}', rooot)
        f = open(pjoin(toPath, 'manage.py'), 'w')
        f.write(str)
        f.close()
        str = open(pjoin(rooot, '.halProject'), 'r').read()
        str = str.replace('baseProject', 'src')
        f = open(pjoin(toPath, '.halProject'), 'w')
        f.write(str)
        f.close()
        if os.path.exists(pjoin(toPath, 'halicea.py')):
            os.rename(pjoin(toPath, 'halicea.py'), pjoin(toPath, 'manage.py'))
        print 'Project is Created!'