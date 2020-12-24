# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/__init__.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 319 bytes
from nlp_model_gen.packages.systemController.SystemController import SystemController
from nlp_model_gen.utils.fileUtils import create_dir_if_not_exist
create_dir_if_not_exist('tmp')
create_dir_if_not_exist('models')
name = 'nlp_model_gen'

def NLPModelAdmin():
    return SystemController()