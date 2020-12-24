# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/evaluator.py
# Compiled at: 2018-12-25 15:18:40
# Size of source mod 2**32: 3468 bytes
import torch, numpy as np, math

def compute_recall(array_pred, array_y):
    return float(len(np.intersect1d(array_pred, array_y))) / len(array_y)


def compute_precision(array_pred, array_y):
    correct_num = [
     0.0] * len(array_pred)
    predict_num = [1.0] * len(array_pred)
    for idx in range(len(correct_num)):
        if array_pred[idx] in array_y:
            correct_num[idx] = 1.0

    weighted_correct = 0.0
    weighted_predict = 0.0
    for idx in range(len(correct_num)):
        weighted_correct += correct_num[idx] / math.log(idx + 3.0)
        weighted_predict += predict_num[idx] / math.log(idx + 3.0)

    return weighted_correct / weighted_predict


def compute_f_score(recall_score, precision_score, f_type=1):
    """
    larget f_type if you prefer high precicion, in most cases, f1 is nice balance in recall and precision.
    """
    coef = 1 + math.pow(f_type, 2)
    pr1 = precision_score + recall_score
    pr2 = math.pow(f_type, 2) * precision_score + recall_score
    if pr2 == 0:
        return 0
    else:
        return coef * pr1 / pr2


class Evaluator(object):

    def __init__(self, criterion, top_k=5):
        self.accumulate_recall = 0.0
        self.accumulate_precision = 0.0
        self.accumulate_f_score = 0.0
        self.accumulate_num_samples = 0
        self.accumulate_loss = 0.0
        self.criterion = criterion
        self.top_k = top_k

    def clear(self):
        self.accumulate_recall = 0.0
        self.accumulate_precision = 0.0
        self.accumulate_f_score = 0.0
        self.accumulate_num_samples = 0
        self.accumulate_loss = 0.0

    def evaluate(self, preds, target, mode='train'):
        """
        do evaluation for each batch
        """
        batch_size = preds.size(0)
        self.accumulate_num_samples += batch_size
        _, preds_idx = torch.topk(preds, k=(self.top_k), dim=1)
        target_value, target_idx = torch.topk(target, k=(self.top_k), dim=1)
        preds_idx_cpu = preds_idx.data.cpu().numpy()
        target_idx_cpu = target_idx.data.cpu().numpy()
        target_value = target_idx.data.cpu().numpy()
        batch_recall = 0.0
        batch_precision = 0.0
        batch_f_score = 0.0
        for idx in range(batch_size):
            ground_truth_num = len(target_value.nonzero())
            _recall = compute_recall(preds_idx_cpu[idx], target_idx_cpu[idx][:ground_truth_num])
            _precition = compute_precision(preds_idx_cpu[idx], target_idx_cpu[idx][:ground_truth_num])
            _f_score = compute_f_score(_recall, _precition)
            batch_recall += _recall
            batch_precision += _precition
            batch_f_score += _f_score

        self.accumulate_recall += batch_recall
        self.accumulate_precision += batch_precision
        self.accumulate_f_score += batch_f_score
        batch_loss = self.criterion(preds, target)
        if mode == 'train':
            batch_loss.backward()
        self.accumulate_loss += batch_loss.item() * batch_size
        return list(map(lambda x: x / self.accumulate_num_samples, [
         self.accumulate_loss,
         self.accumulate_recall,
         self.accumulate_precision,
         self.accumulate_f_score]))