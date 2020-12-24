# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hyperkite/__init__.py
# Compiled at: 2020-03-31 07:39:44
# Size of source mod 2**32: 295 bytes
from hyperkite.hyperkite import Study, Trial

def new_trial(study_key: str):
    study = Study(study_key)
    trial = study.new_trial()
    return trial


def get_best_values(study_key: str):
    study = Study(study_key)
    best_trial = study.get_best_trial()
    return best_trial.values