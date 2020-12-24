# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/run/alpha.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 2862 bytes
import traceback, numpy as np, tensorflow as tf
from tensorflow import keras
from ....search import util
from trainer.train_valid import TrainerTrainValid
from .util import compute_objective, load_config, preproc_trainer, setup_data, setup_search_space
logger = util.conf_logger('deephyper.search.nas.run')
default_callbacks_config = {'EarlyStopping':dict(monitor='val_loss',
   min_delta=0,
   mode='min',
   verbose=0,
   patience=0), 
 'TensorBoard':dict(log_dir='',
   histogram_freq=0,
   batch_size=32,
   write_graph=False,
   write_grads=False,
   write_images=False,
   update_freq='epoch')}

def run(config):
    seed = config['seed']
    if seed is not None:
        np.random.seed(seed)
        tf.random.set_random_seed(seed)
    else:
        load_config(config)
        input_shape, output_shape = setup_data(config)
        search_space = setup_search_space(config, input_shape, output_shape, seed=seed)
        model_created = False
        try:
            model = search_space.create_model()
            model_created = True
        except:
            logger.info('Error: Model creation failed...')
            logger.info(traceback.format_exc())

        if model_created:
            callbacks = []
            cb_requires_valid = False
            callbacks_config = config['hyperparameters'].get('callbacks')
            if callbacks_config is not None:
                for cb_name, cb_conf in callbacks_config.items():
                    if cb_name in default_callbacks_config:
                        default_callbacks_config[cb_name].update(cb_conf)
                        if cb_name == 'ModelCheckpoint':
                            default_callbacks_config[cb_name]['filepath'] = f"best_model_{config['id']}.h5"
                        Callback = getattr(keras.callbacks, cb_name)
                        callbacks.append(Callback(**default_callbacks_config[cb_name]))
                        if cb_name in ('EarlyStopping', ):
                            cb_requires_valid = 'val' in cb_conf['monitor'].split('_')
                    else:
                        logger.error(f"'{cb_name}' is not an accepted callback!")

            trainer = TrainerTrainValid(config=config, model=model)
            trainer.callbacks.extend(callbacks)
            last_only, with_pred = preproc_trainer(config)
            last_only = last_only and not cb_requires_valid
            history = trainer.train(with_pred=with_pred, last_only=last_only)
            result = compute_objective(config['objective'], history)
        else:
            result = -1
    return result