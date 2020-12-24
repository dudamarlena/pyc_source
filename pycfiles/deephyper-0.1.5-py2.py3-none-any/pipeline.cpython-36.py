# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/post/pipeline.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 2753 bytes
import json, sys, traceback
from time import time
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import load_model
from deephyper.evaluator import Encoder
from deephyper.search import util
from deephyper.search.nas.model.run.util import load_config, setup_data, setup_structure, compute_objective
from deephyper.search.nas.model.trainer.train_valid import TrainerTrainValid
logger = util.conf_logger(__name__)
default_cfg = {'model_checkpoint':dict(monitor='val_loss',
   mode='min',
   save_best_only=True,
   verbose=1), 
 'early_stopping':dict(monitor='val_loss',
   mode='min',
   verbose=1,
   patience=50)}

def train(config):
    keys = filter(lambda k: k in config['hyperparameters'], config['post_train'].keys())
    for k in keys:
        config['hyperparameters'][k] = config['post_train'][k]

    keys = filter(lambda k: k in default_cfg, config['post_train'].keys())
    for k in keys:
        default_cfg[k] = config['post_train'][k]

    load_config(config)
    input_shape, output_shape = setup_data(config)
    structure = setup_structure(config, input_shape, output_shape)
    structure.draw_graphviz(f"structure_{config['id']}.dot")
    logger.info('Model operations set.')
    model_created = False
    try:
        model = structure.create_model()
        model_created = True
    except:
        model_created = False
        logger.info('Error: Model creation failed...')
        logger.info(traceback.format_exc())

    if model_created:
        trainer = TrainerTrainValid(config=config, model=model)
    if model_created:
        trainer.callbacks.append(EarlyStopping(**default_cfg['early_stopping']))
        trainer.callbacks.append(ModelCheckpoint(
         f"best_model_{config['id']}.h5", **default_cfg['model_checkpoint']))
        json_fname = f"post_training_hist_{config['id']}.json"
        trainer.init_history()
        with open(json_fname, 'w') as (f):
            json.dump((trainer.train_history), f, cls=Encoder)
        hist = trainer.train(with_pred=False, last_only=False)
        t = time()
        trainer.predict(dataset='valid')
        hist['val_predict_time'] = time() - t
        with open(json_fname, 'w') as (f):
            json.dump(hist, f, cls=Encoder)