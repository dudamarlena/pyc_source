# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/versionning/base.py
# Compiled at: 2010-05-21 08:57:51
from tg import config
from pyf.services.model import Tube, TubeLayer, Descriptor, DBSession
from pyjon.versionning import SARepository

def get_repo_folder():
    return config.get('versionning.repository', './repo')


def get_repository():
    return SARepository(get_repo_folder(), DBSession, [Tube,
     TubeLayer,
     Descriptor])