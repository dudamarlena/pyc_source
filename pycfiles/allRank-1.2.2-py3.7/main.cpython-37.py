# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/main.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 4117 bytes
import os
from argparse import ArgumentParser, Namespace
from functools import partial
from pprint import pformat
import numpy as np, torch
from attr import asdict
from torch import optim
import allrank.models.losses as losses
from allrank.config import Config
from allrank.data.dataset_loading import load_libsvm_dataset, create_data_loaders
from allrank.models.model import make_model
from allrank.models.model_utils import get_torch_device, CustomDataParallel
from allrank.training.train_utils import fit
from allrank.utils.command_executor import execute_command
from allrank.utils.experiments import dump_experiment_result, assert_expected_metrics
from allrank.utils.file_utils import create_output_dirs, PathsContainer
from allrank.utils.ltr_logging import init_logger
from allrank.utils.python_utils import dummy_context_mgr

def parse_args() -> Namespace:
    parser = ArgumentParser('allRank')
    parser.add_argument('--job-dir', help='Base output path for all experiments', required=True)
    parser.add_argument('--run-id', help='Name of this run to be recorded (must be unique within output dir)', required=True)
    parser.add_argument('--config-file-name', required=True, type=str, help='Name of json file with config')
    return parser.parse_args()


def run():
    torch.manual_seed(42)
    torch.cuda.manual_seed_all(42)
    np.random.seed(42)
    args = parse_args()
    paths = PathsContainer.from_args(args.job_dir, args.run_id, args.config_file_name)
    os.makedirs((paths.base_output_path), exist_ok=True)
    create_output_dirs(paths.output_dir)
    logger = init_logger(paths.output_dir)
    logger.info('will save data in {output_dir}'.format(output_dir=(paths.base_output_path)))
    config = Config.from_json(paths.config_path)
    logger.info('Config:\n {}'.format(pformat((vars(config)), width=1)))
    output_config_path = os.path.join(paths.output_dir, 'used_config.json')
    execute_command('cp {} {}'.format(paths.config_path, output_config_path))
    train_ds, val_ds = load_libsvm_dataset(input_path=(config.data.path),
      slate_length=(config.data.slate_length),
      validation_ds_role=(config.data.validation_ds_role))
    n_features = train_ds.shape[(-1)]
    if not n_features == val_ds.shape[(-1)]:
        raise AssertionError('Last dimensions of train_ds and val_ds do not match!')
    else:
        train_dl, val_dl = create_data_loaders(train_ds,
          val_ds, num_workers=(config.data.num_workers), batch_size=(config.data.batch_size))
        dev = get_torch_device()
        logger.info('Model training will execute on {}'.format(dev.type))
        model = make_model(**asdict((config.model), recurse=False), **{'n_features': n_features})
        if torch.cuda.device_count() > 1:
            model = CustomDataParallel(model)
            logger.info('Model training will be distributed to {} GPUs.'.format(torch.cuda.device_count()))
        model.to(dev)
        optimizer = (getattr(optim, config.optimizer.name))(params=model.parameters(), **config.optimizer.args)
        loss_func = partial((getattr(losses, config.loss.name)), **(config.loss).args)
        if config.lr_scheduler.name:
            scheduler = (getattr(optim.lr_scheduler, config.lr_scheduler.name))(optimizer, **(config.lr_scheduler).args)
        else:
            scheduler = None
    with torch.autograd.detect_anomaly() if config.detect_anomaly else dummy_context_mgr():
        result = fit(**asdict(config.training), **{'model':model, 
         'loss_func':loss_func, 
         'optimizer':optimizer, 
         'scheduler':scheduler, 
         'train_dl':train_dl, 
         'valid_dl':val_dl, 
         'config':config, 
         'device':dev, 
         'output_dir':paths.output_dir, 
         'tensorboard_output_path':paths.tensorboard_output_path})
    dump_experiment_result(args, config, paths.output_dir, result)
    assert_expected_metrics(result, config.expected_metrics)


if __name__ == '__main__':
    run()