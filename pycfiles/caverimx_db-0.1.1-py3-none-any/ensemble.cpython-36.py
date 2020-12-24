# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/ensemble.py
# Compiled at: 2018-12-25 02:14:51
# Size of source mod 2**32: 3920 bytes
import numpy as np, torch, torch.nn.functional as F

class EnsembleException(Exception):
    pass


class EnsembleModel(object):
    """EnsembleModel"""

    def __init__(self, models):
        assert isinstance(models, list) and len(models) > 0
        self.model_consistance_checker(models)
        self.models = models
        self.labels = models[0]._inside_model.labels
        self.vocab = models[0]._inside_model.vocab
        self.epsilon = 1e-08
        self.methods = {'mean':self.mean, 
         'log':self.log, 
         'hmean':self.hmean, 
         'gmean':self.gmean}

    def __str__(self):
        start = '====== ensemble summary =======\n'
        summary = '\n-------------\n'.join([model.__str__() for model in self.models])
        return start + summary

    def model_consistance_checker(self, models):
        for model in models:
            if model._inside_model.labels != models[0]._inside_model.labels:
                raise EnsembleException('all models in ensemble mode should have same labels and vocab dict')
            if model._inside_model.vocab != models[0]._inside_model.vocab:
                raise EnsembleException('all models in ensemble mode should have same labels and vocab dict')

    def mean(self, models_preds):
        ensemble_batch_preds = torch.zeros(models_preds[0].shape)
        for preds in models_preds:
            ensemble_batch_preds += preds

        ensemble_batch_preds = ensemble_batch_preds / len(self.models)
        return ensemble_batch_preds

    def log(self, preds):
        return np.exp(np.log(self.epsilon + preds).mean(axis=0))

    def hmean(self, models_preds):
        ensemble_batch_preds = torch.zeros(models_preds[0].shape)
        for preds in models_preds:
            ensemble_batch_preds += 1 / preds

        ensemble_batch_preds = len(self.models) / ensemble_batch_preds
        return ensemble_batch_preds

    def gmean(self, models_preds):
        ensemble_batch_preds = torch.ones(models_preds[0].shape)
        for preds in models_preds:
            ensemble_batch_preds *= preds

        ensemble_batch_preds = ensemble_batch_preds ** (1 / len(self.models))
        return ensemble_batch_preds

    def _predict_text(self, batch_sequence_text, device='cpu', top_k=5, method='mean'):
        """
        :param str text: text
        :param str method: ['mean', 'hmean', 'gmean']

        mean: arithmetic mean
        hmean: harmonica mean
        gmean: geometric mean

        """
        models_preds = [model._inside_model._get_model_output(batch_sequence_text=batch_sequence_text, vocab_dict=(self.vocab), device='cpu') for model in self.models]
        models_preds_softmax = [F.softmax(preds, dim=1) for preds in models_preds]
        ensemble_batch_preds = self.methods[method](models_preds_softmax)
        batch_top_k_value, batch_top_k_index = torch.topk((torch.sigmoid(ensemble_batch_preds)), k=top_k, dim=1)
        return batch_top_k_index

    def predict(self, batch_sequence_text, top_k=5, method='mean'):
        batch_top_k_index = self._predict_text(batch_sequence_text, top_k=5, method='mean')
        batch_top_k_index = batch_top_k_index.data.cpu().numpy()
        labels = []
        for pred in batch_top_k_index:
            labels.append([self.labels[idx] for idx in pred])

        return labels