# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ood_metrics/metrics.py
# Compiled at: 2020-01-10 16:16:46
# Size of source mod 2**32: 3965 bytes
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt
import numpy as np

def auroc(preds, labels):
    """Calculate and return the area under the ROC curve using unthresholded predictions on the data and a binary true label.
    
    preds: array, shape = [n_samples]
           Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of decisions.
           
    labels: array, shape = [n_samples]
            True binary labels in range {0, 1} or {-1, 1}.
    """
    fpr, tpr, _ = roc_curve(labels, preds)
    return auc(fpr, tpr)


def aupr(preds, labels):
    """Calculate and return the area under the Precision Recall curve using unthresholded predictions on the data and a binary true label.
    
    preds: array, shape = [n_samples]
           Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of decisions.
           
    labels: array, shape = [n_samples]
            True binary labels in range {0, 1} or {-1, 1}.
    """
    precision, recall, _ = precision_recall_curve(labels, preds)
    return auc(recall, precision)


def fpr_at_95_tpr(preds, labels):
    """Return the FPR when TPR is at minimum 95%.
        
    preds: array, shape = [n_samples]
           Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of decisions.
           
    labels: array, shape = [n_samples]
            True binary labels in range {0, 1} or {-1, 1}.
    """
    fpr, tpr, _ = roc_curve(labels, preds)
    if all(tpr < 0.95):
        return 0
    if all(tpr >= 0.95):
        idxs = [i for i, x in enumerate(tpr) if x >= 0.95]
        return min(map(lambda idx: fpr[idx], idxs))
    return np.interp(0.95, tpr, fpr)


def detection_error(preds, labels):
    """Return the misclassification probability when TPR is 95%.
        
    preds: array, shape = [n_samples]
           Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of decisions.
           
    labels: array, shape = [n_samples]
            True binary labels in range {0, 1} or {-1, 1}.
    """
    fpr, tpr, _ = roc_curve(labels, preds)
    f2t_ratio = sum(np.array(labels) == 1) / len(labels)
    t2f_ratio = 1 - f2t_ratio
    idxs = [i for i, x in enumerate(tpr) if x >= 0.95]
    _detection_error = lambda idx: t2f_ratio * (1 - tpr[idx]) + f2t_ratio * fpr[idx]
    return min(map(_detection_error, idxs))


def calc_metrics(predictions, labels):
    """Using predictions and labels, return a dictionary containing all novelty
    detection performance statistics.
    
    These metrics conform to how results are reported in the paper 'Enhancing The 
    Reliability Of Out-of-Distribution Image Detection In Neural Networks'.
    
        preds: array, shape = [n_samples]
           Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of decisions.
           
    labels: array, shape = [n_samples]
            True binary labels in range {0, 1} or {-1, 1}.
    """
    return {'fpr_at_95_tpr':fpr_at_95_tpr(predictions, labels), 
     'detection_error':detection_error(predictions, labels), 
     'auroc':auroc(predictions, labels), 
     'aupr_in':aupr(predictions, labels), 
     'aupr_out':aupr([-a for a in predictions], [1 - a for a in labels])}