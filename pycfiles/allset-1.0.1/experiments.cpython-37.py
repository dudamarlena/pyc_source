# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/utils/experiments.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 1707 bytes
import json, os
from argparse import Namespace
from typing import Dict, Any
from attr import asdict
from flatten_dict import flatten
from allrank.config import Config
from allrank.utils.ltr_logging import get_logger
logger = get_logger()

def unpack_numpy_values(dict):
    return {k:v.item() for k, v in dict.items()}


def dump_experiment_result(args: Namespace, config: Config, output_dir: str, result: Dict[(str, Any)]):
    final_config_dict = asdict(config)
    flattened_experiment = flatten(final_config_dict, reducer='path')
    result['train_metrics'] = unpack_numpy_values(result['train_metrics'])
    result['val_metrics'] = unpack_numpy_values(result['val_metrics'])
    result['num_params'] = result['num_params'].item()
    flattened_result = flatten(result, reducer='path')
    flattened_experiment.update(flattened_result)
    flattened_experiment['run_id'] = args.run_id
    flattened_experiment['dir'] = output_dir
    with open(os.path.join(output_dir, 'experiment_result.json'), 'w') as (json_file):
        json.dump(flattened_experiment, json_file)
        json_file.write('\n')


def assert_expected_metrics(result: Dict[(str, Any)], expected_metrics: Dict[(str, Dict[(str, float)])]):
    if expected_metrics:
        for role, metrics in expected_metrics.items():
            for name, expected_value in metrics.items():
                actual_value = result['{}_metrics'.format(role)][name]
                msg = '{} {} got {}. It was expected to be at least {}'.format(role, name, actual_value, expected_value)
                if actual_value < expected_value:
                    logger.info(msg)
                assert actual_value >= expected_value, msg