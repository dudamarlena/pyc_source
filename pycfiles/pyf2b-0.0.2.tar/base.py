# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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