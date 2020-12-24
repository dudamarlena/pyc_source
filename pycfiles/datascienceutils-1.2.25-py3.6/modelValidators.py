# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/modelValidators.py
# Compiled at: 2017-12-07 08:54:26
# Size of source mod 2**32: 3243 bytes
import json
from . import statsutils as su

def validate(model, model_info_or_file, input_data):
    if not isinstance(model_info_or_file, dict):
        with open(model_info, 'r') as (fd):
            model_info = json.load(fd)
    else:
        model_info = model_info_or_file
    if not 'input_metadata' in model_info:
        raise AssertionError('Input metadata missing in model info')
    else:
        if not 'output_metadata' in model_info:
            raise AssertionError('Output metadata missing in model info')
        elif not 'output_type' in model_info:
            raise AssertionError('Output type required')
        assert 'model_class' in model_info, 'Model Class (multi-class/single-class/regression) required'
    print('Input dist tests')
    for col in input_data.columns:
        dist = model_info['input_metadata'][col]['dist']
        su.distribution_similarity((input_data[col].tolist()), dist_type=dist)

    predictions = model.predict(input_data)
    series = predictions
    if model_info.get('model_class', None) == 'regression':
        if model_info.get('output_metadata', None):
            dist = model_info['output_metadata']['dist']
        else:
            dist = 'norm'
        print('Output dist tests')
        test_results = su.distribution_similarity(series, dist)
        print(test_results)
    if model_info.get('model_class', None) == 'multiclass':
        print('Output dist tests')
        n_classes = model_info['output_metadata']['n_classes']
        class_probs = model_info['output_metadata']['class_probs']
        assert n_classes == len(class_probs), 'n_classes must equal length of class_probs'
        dist = stats.multinomial(len(input_data), class_probs)
        test_results = su.distribution_similarity(series, dist)
    if model_info.get('model_class', None) == 'singleclass':
        print('Output dist tests')
        prob = model_info['output_metadata']['success_prob']
        dist = stats.binom(len(input_data), prob)
        test_results = su.distribution_similarity(series, dist)
    if model_info.get('input_metadata', None):
        input_dists = model_info['input_metadata']
        for col, dist in input_dists.items():
            series = input_data[col].tolist()
            dist = dist['dist']
            test_results = su.distribution_similarity(series, dist)

    print(test_results)