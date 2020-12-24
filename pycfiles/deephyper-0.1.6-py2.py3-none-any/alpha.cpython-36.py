# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/run/alpha.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 1198 bytes
import traceback, numpy as np
from deephyper.search import util
from deephyper.search.nas.model.run.util import compute_objective, load_config, preproc_trainer, setup_data, setup_structure
from deephyper.search.nas.model.trainer.train_valid import TrainerTrainValid
logger = util.conf_logger('deephyper.search.nas.run')

def run(config):
    load_config(config)
    input_shape, output_shape = setup_data(config)
    structure = setup_structure(config, input_shape, output_shape)
    model_created = False
    try:
        model = structure.create_model()
        model_created = True
    except:
        logger.info('Error: Model creation failed...')
        logger.info(traceback.format_exc())

    if model_created:
        trainer = TrainerTrainValid(config=config, model=model)
        last_only, with_pred = preproc_trainer(config)
        history = trainer.train(with_pred=with_pred, last_only=last_only)
        result = compute_objective(config['objective'], history)
    else:
        result = -1
    return result