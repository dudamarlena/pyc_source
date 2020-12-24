# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/context.py
# Compiled at: 2018-06-21 09:54:43
# Size of source mod 2**32: 4127 bytes
import os, shutil
from flame.util import utils
from flame.predict import Predict
from flame.build import Build
import multiprocessing as mp
MAX_MODELS_SINGLE_CPU = 4

def get_external_input(task, model_set, infile):
    """
    Manage obtention of input data from external
    data sources (e.g. models or MD servers)
    """
    parallel = len(model_set) > MAX_MODELS_SINGLE_CPU
    if parallel:
        task.set_single_CPU()
    else:
        for mi in model_set:
            mi['infile'] = infile

        model_suc = []
        model_res = []
        if parallel:
            pool = mp.Pool(len(model_set))
            model_temp = pool.map(predict_cmd, model_set)
            for x in model_temp:
                model_suc.append(x[0])
                model_res.append(x[1])

        else:
            for mi in model_set:
                success, results = predict_cmd(mi)
                model_suc.append(success)
                model_res.append(results)

    if False in model_suc:
        return (False, 'Some external input sources failed: ', str(model_suc))
    else:
        return (
         True, model_res)


def predict_cmd(model, output_format=None):
    """
    Instantiates a Predict object to run a prediction using the given input
    file and model.

    This method must be self-contained and suitable for being called in
    cascade, by models which use the output of other models as input.
    """
    predict = Predict(model['endpoint'], model['version'], output_format)
    ext_input, model_set = predict.get_model_set()
    if ext_input:
        success, model_res = get_external_input(predict, model_set, model['infile'])
        if not success:
            return (
             False, model_res)
        success, results = predict.run(model_res)
    else:
        success, results = predict.run(model['infile'])
    return (success, results)


def build_cmd(model, output_format=None):
    """
    Instantiates a Build object to build a model using the given
    input file and model. 

    This method must be self-contained and suitable for being called in
    cascade, by models which use the output of other models as input
    """
    build = Build(model['endpoint'], output_format)
    ext_input, model_set = build.get_model_set()
    if ext_input:
        success, model_res = get_external_input(build, model_set, model['infile'])
        if not success:
            return (
             False, model_res)
        success, results = build.run(model_res)
    else:
        ifile = model['infile']
        if not os.path.isfile(ifile):
            return (False, 'wrong training series file')
        epd = utils.model_path(model['endpoint'], 0)
        lfile = os.path.join(epd, os.path.basename(ifile))
        shutil.copy(ifile, lfile)
        success, results = build.run(lfile)
    return (success, results)