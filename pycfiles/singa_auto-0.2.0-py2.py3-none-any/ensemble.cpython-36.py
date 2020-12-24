# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/predictor/ensemble.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 2316 bytes
import logging, numpy as np
from typing import List, Callable, Any
logger = logging.getLogger(__name__)

def get_ensemble_method(task: str='') -> Callable[([List[Any]], Any)]:
    if task == 'IMAGE_CLASSIFICATION':
        return ensemble_probabilities
    else:
        return ensemble


def ensemble_probabilities(predictions: List[Any]) -> Any:
    if len(predictions) == 0:
        return
    else:
        probs_by_worker = predictions
        assert all([len(x) == len(probs_by_worker[0]) for x in probs_by_worker])
        if not isinstance(predictions[0], dict):
            probs = np.mean(probs_by_worker, axis=0)
            prediction = probs
            prediction = _simplify_prediction(prediction)
        else:
            prediction = predictions
        return prediction


def ensemble(predictions: List[Any]) -> Any:
    if len(predictions) == 0:
        return
    else:
        print('predictions is (in ensemble)', predictions)
        index = 0
        prediction = predictions[index]
        prediction = _simplify_prediction(prediction)
        return prediction


def _simplify_prediction(prediction):
    if isinstance(prediction, np.ndarray):
        prediction = prediction.tolist()
    if isinstance(prediction, list):
        for i, x in enumerate(prediction):
            prediction[i] = _simplify_prediction(x)

    return prediction